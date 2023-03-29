"""
Реазлиция презентера расходов
Наследуется от презентера таблиц
"""
from bookkeeper.view.table_presenter import Generic_Table
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.category import Category


class Expense_Presenter(Generic_Table):
    """
    Класс презентера расходов
    """

    def __init__(self, cat_repo: AbstractRepository[Category], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cat_repo = cat_repo
