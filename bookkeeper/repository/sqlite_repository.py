"""
Модуль описывает репозиторий, работающий с библиотекой SQLite3

"""
import sqlite3

from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T
from typing import Any


class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: type) -> None:
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.names = ', '.join(self.fields.keys())
        self.filler = ', '.join("?" * len(self.fields))
        self.cls = cls

    def table_converter(self, fields: dict[str, Any]) -> str:
        """
        Вспомогательная функция, форматирующая
        запросы sql
        """
        result = '('
        for key, value in fields.items():
            result += key
            if 'str' in str(value):
                result += ' TEXT'
            if 'int' in str(value):
                result += ' INTEGER'
            if 'datetime' in str(value):
                result += ' DATETIME'
            result += ', '
        return result[:-2] + ')'

    def add(self, obj: T) -> int:
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'CREATE TABLE IF NOT EXISTS {self.table_name} ' +
                self.table_converter(self.fields)
            )
            cur.execute(
                f'INSERT INTO {self.table_name} ({self.names}) VALUES ({self.filler})',
                values
            )
            pk = cur.lastrowid
        con.close()
        if pk is None:
            raise ValueError
        return pk

    def get(self, pk: int) -> T | None:
        result = None
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            try:
                cur.execute(f'SELECT *, rowid FROM {self.table_name}' +
                            f' WHERE rowid = {pk}')
                records = cur.fetchall()
                result = self.cls(*records[0])  # unpack List[Tuple]
            except sqlite3.OperationalError as exc:
                print(exc)
                print('Элемента не существует')
                result = None
            except IndexError:
                result = None
        con.close()
        return result

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        if where is None:
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                cur.execute('PRAGMA foreign_keys = ON')
                try:
                    cur.execute(f'SELECT *, rowid FROM {self.table_name}')
                    allresult = cur.fetchall()
                    result = []
                    for element in allresult:
                        result.append(self.cls(*element))
                except sqlite3.OperationalError:
                    print('Элементов не найдено')
                    result = []
            con.close()
        else:
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                names = ', '.join(where.keys())
                values = "'" + "', '".join(where.values()) + "'"
                try:
                    cur.execute('PRAGMA foreign_keys = ON')
                    cur.execute(
                        f'SELECT *, rowid FROM {self.table_name}' +
                        f' WHERE ({names}) = ({values});'
                    )
                    allresult = cur.fetchall()
                    result = []
                    for element in allresult:
                        result.append(self.cls(*element))
                except sqlite3.OperationalError:
                    print('The table probably does not exist. Try to add smth first.')
                    result = []
            con.close()
        return result

    def update(self, obj: T) -> None:
        """
        Обновление записи
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            names = ', '.join(self.fields.keys())
            filler = ', '.join("?" * len(self.fields))
            values = [getattr(obj, x) for x in self.fields]
            try:
                cur.execute(
                    f'UPDATE {self.table_name} SET ({names}) = ({filler})' +
                    f'WHERE rowid = {obj.pk}',
                    values
                )
            except sqlite3.OperationalError as exc:
                print(exc)
                print('Записи ещё не существует')
            if obj.pk is None:
                raise TypeError
        con.close()

    def delete(self, pk: int) -> None:
        """
        Удаление записи
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            try:
                cur.execute(f'DELETE FROM {self.table_name} WHERE rowid = {pk}')
                if cur.rowcount == 0:
                    raise KeyError('Записи не существует')
            except sqlite3.OperationalError as exc:
                print(exc)
                print('Записи ещё не существует')
        con.close()

