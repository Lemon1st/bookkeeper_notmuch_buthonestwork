"""
Здесь реализован презентер бюджета и соответствующий расчёт
"""
from PySide6 import QtWidgets
from bookkeeper.view.table_presenter import Generic_Table
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense


class Budget_Presenter(QtWidgets.QWidget):
    """
    Класс таблицы бюджета
    Для непосредственного расчёта необходимо брать данные
    из других классов
    """
    def __init__(self, budget_repo: AbstractRepository[Budget],
                 expense_repo: AbstractRepository[Expense],
                 table_name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.expense_repo = expense_repo
        self.budget_repo = budget_repo
        self.layout = QtWidgets.QVBoxLayout()
        self.table = Generic_Table(budget_repo, table_name)
        self.table.refresh_click()
        self.layout.addWidget(self.table)
        calculate_button = QtWidgets.QPushButton('Рассчёт бюджета')
        self.layout.addWidget(calculate_button)
        calculate_button.clicked.connect(self.calculate_budget)
        self.setLayout(self.layout)

    def calculate_budget(self) -> None:
        """
        Рассчёт бюджета
        """
        data = self.expense_repo.get_all()
        for period in self.budget_repo.get_all():
            current_value = period
            current_value.expense_over_period = period.calculate(data)
            self.budget_repo.update(current_value)
        self.table.refresh_click()
