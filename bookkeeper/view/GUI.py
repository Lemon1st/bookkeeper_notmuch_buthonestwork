"""
Итоговый графический интерфейс с модульной реализацией
К основному окну подключаются таблицы соответствующих модулей
Модули сделаны по аналогии друг с другом с 
учетом характерных особенностей задач
"""
from PySide6 import QtWidgets
from bookkeeper.view.table_presenter import Generic_Table
from bookkeeper.view.budget_presenter import Budget_Presenter
from bookkeeper.view.expense_presenter import Expense_Presenter
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense


class GUI(QtWidgets.QWidget):
    """
    Графический интерфейс
    """
    def __init__(self, expense_db: AbstractRepository[Expense],
                 category_db: AbstractRepository[Category],
                 budget_db: AbstractRepository[Budget], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Менеджер расходов')
        self.layout = QtWidgets.QVBoxLayout()
        self.table1 = Expense_Presenter(category_db, expense_db, 'Расходы')
        self.layout.addWidget(self.table1)
        self.table1.refresh_click()
        self.table2 = Budget_Presenter(budget_db, expense_db, 'Бюджет')
        self.layout.addWidget(self.table2)
        self.setLayout(self.layout)
        self.table3 = Generic_Table(category_db, 'Категории расходов')
        self.layout.addWidget(self.table3)
        self.table3.refresh_click()

