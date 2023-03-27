"""
Модуль описывает репозиторий, работающий с библиотекой SQLite3

"""
import sqlite3

from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T
from typing import Any


class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.cls = cls
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            res = cur.execute('SELECT name FROM sqlite_master')
            db_tables = [t[0].lower() for t in res.fetchall()]
            if self.table_name not in db_tables:
                col_names = ', '.join(self.fields.keys())
                q = f'CREATE TABLE {self.table_name} (' \
                    f'"pk" INTEGER PRIMARY KEY AUTOINCREMENT, {col_names})'
                cur.execute(q)
        con.close()

    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            q = f'INSERT INTO {self.table_name} ({names}) VALUES ({p})'
            cur.execute(q, values)
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            q = f'SELECT * FROM {self.table_name} WHERE pk = {pk}'
            row = cur.execute(q).fetchone()
        con.close()

        if row is None:
            return None

        obj = self.cls()
        for field, value in zip(self.fields, row[1:]):
            setattr(obj, field, value)
        obj.pk = pk
        return obj

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'SELECT * FROM {self.table_name}')  # TODO: добавить блок WHERE
            res = cur.fetchall()
        con.close()
        return res

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
            cur.execute(
                f'UPDATE {self.table_name} SET ({names}) = ({filler})' +
                f'WHERE rowid = {obj.pk}',
                values
            )
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
            cur.execute(f'DELETE FROM {self.table_name} WHERE rowid = {pk}')

        con.close()
