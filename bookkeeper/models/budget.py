"""
Описан класс, представляющий описание бюджета
"""
from dataclasses import dataclass, field
from datetime import datetime
from bookkeeper.models.expense import Expense


@dataclass(slots=True)
class Budget:
    """
    Бюджет (расходы за период времени).
    name - название периода (например: "Бюджет на месяц)
    begin_period_date - дата начала отсчета
    end_period_date - дата конца отсчета
    expense_over_period - все расходоы за данный период
    comment - комментарий
    pk - id в базе данных
    """

    name: str = 'Период'
    begin_period_date: datetime = field(default_factory=datetime.now)
    end_period_date: datetime = field(default_factory=datetime.now)
    expense_over_period: int = 0
    comment: str = ''
    pk: int = 0
