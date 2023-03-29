"""
Итоговый графический интерфейс с модульной реализацией
К основному окну подключаются таблицы соответствующих модулей
Модули сделаны по аналогии друг с другом с 
учетом характерных особенностей задач
"""
from PySide6 import QtWidgets
from bookkeeper.view.expense_presenter import Expense_Presenter
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense


class GUI(QtWidgets.QWidget):
    """
    Графический интерфейс
    """
    def __init__(self, expense_db: AbstractRepository[Expense],
                 category_db: AbstractRepository[Category],
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Менеджер расходов')
        self.layout = QtWidgets.QVBoxLayout()
        self.table1 = Expense_Presenter(category_db, expense_db, 'Расходы')
        self.layout.addWidget(self.table1)
        self.table1.refresh_click()

