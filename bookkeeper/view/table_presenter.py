"""
Реализация общего класса таблиц, так как они ведут себя схожим образом
Также реализация элементов графического интерфейса и взаимодействия
с ним
"""

from PySide6 import QtWidgets
from bookkeeper.repository.abstract_repository import AbstractRepository, T


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
