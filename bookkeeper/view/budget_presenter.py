"""
Здесь реализован презентер бюджета
"""
from PySide6 import QtWidgets
from bookkeeper.view.table_presenter import Generic_Table
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.budget import Budget


class Budget_Presenter(QtWidgets.QWidget):
    """
    Класс таблицы бюджета
    Для непосредственного расчёта необходимо брать данные
    из других классов
    """
    def __init__(self, budget_repo: AbstractRepository[Budget],
                 table_name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.budget_repo = budget_repo
        self.layout = QtWidgets.QVBoxLayout()
        self.table = Generic_Table(budget_repo, table_name)
        self.table.refresh_click()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
