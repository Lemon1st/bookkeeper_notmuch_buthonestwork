"""
Реализация общего класса таблиц, так как они ведут себя схожим образом
Также реализация элементов графического интерфейса и взаимодействия
с ним
"""

from PySide6 import QtWidgets
from bookkeeper.repository.abstract_repository import AbstractRepository, T
from PySide6.QtCore import QDateTime


class Generic_Table(QtWidgets.QWidget):
    """
    Класс таблиц
    """

    def __init__(self, repo: AbstractRepository[T],
                 name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.repo = repo
        self.layout = QtWidgets.QGridLayout()
        # Элементы графического интерфейса, общие для любого вида таблиц
        self.name = QtWidgets.QLabel(name)
        self.layout.addWidget(self.name, 0, 0, 1, 1)

        self.add_button = QtWidgets.QPushButton('Добавить')
        self.add_button.clicked.connect(self.add_menu)
        self.layout.addWidget(self.add_button, 0, 1, 1, 1)

        self.delete_button = QtWidgets.QPushButton('Удалить')
        self.delete_button.clicked.connect(self.del_menu)
        self.layout.addWidget(self.delete_button, 0, 2, 1, 1)

        self.update_button = QtWidgets.QPushButton('Изменить запись')
        self.update_button.clicked.connect(self.update_menu)
        self.layout.addWidget(self.update_button, 0, 3, 1, 1)
        # Создание заголовков таблиц при считывании категорий
        try:
            self.exp_tabl = QtWidgets.QTableWidget(20, len(self.repo.fields) + 1)
            names = ', '.join(self.repo.fields.keys())
            for i, element in enumerate(names.split(',')):
                self.exp_tabl.setHorizontalHeaderItem(
                    i, QtWidgets.QTableWidgetItem(element)
                )
            self.exp_tabl.setHorizontalHeaderItem(
                len(self.repo.fields),
                QtWidgets.QTableWidgetItem('PK')
            )
            self.layout.addWidget(self.exp_tabl, 1, 0, 1, 60)
            self.setLayout(self.layout)
        except AttributeError as err:
            print('Невозможно получить атрибут', err)
        self.dialog = QtWidgets.QDialog()
        self.table_widgets = []

    def add_data(self, data: list) -> None:
        """
        Заполнение таблицы элементами, вспомогательная функция
        """
        for ii, row in enumerate(data):
            for jj, x in enumerate(row):
                self.exp_tabl.setItem(
                    ii, jj,
                    QtWidgets.QTableWidgetItem(str(x))
                )
                self.exp_tabl.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def refresh_click(self) -> None:
        """
        Функция, реализующее обновление элементов при
        нажатии на кнопку обновления
        """
        result = self.repo.get_all()
        add_table = []
        for element in result:
            values = [getattr(element, x) for x in self.repo.fields]
            values.append(getattr(element, 'pk'))
            add_table.append(values)
        self.exp_tabl.clearContents()
        self.add_data(add_table)

    def cancel(self) -> None:
        """
        Закрытие диалогового окна или отмена
        """
        self.dialog.close()

    def add_menu(self) -> None:
        """
        Меню и кнопки, добавляющие элемент
        """
        self.dialog = QtWidgets.QDialog()
        layout = QtWidgets.QGridLayout()
        self.table_widgets = []
        for i, element in enumerate(self.repo.fields):
            if element == 'category':
                self.table_widgets.append(QtWidgets.QComboBox())
                self.set_categories()
            elif 'date' in element:
                self.table_widgets.append(QtWidgets.QDateTimeEdit())
                self.table_widgets[-1].setDateTime(QDateTime.currentDateTime())
            else:
                self.table_widgets.append(QtWidgets.QLineEdit())
            layout.addWidget(QtWidgets.QLabel(str(element)), i, 0)
            layout.addWidget(self.table_widgets[-1], i, 1)
        add = QtWidgets.QPushButton('Добавить')
        cancel = QtWidgets.QPushButton('Отменить')
        cancel.clicked.connect(self.cancel)
        add.clicked.connect(self.add_click)
        layout.addWidget(add, len(self.repo.fields)+1, 0)
        layout.addWidget(cancel, len(self.repo.fields)+1, 1)
        self.dialog.setLayout(layout)
        self.dialog.setWindowTitle('Добавить запись')
        self.dialog.exec()
