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

    def calculate(self, data: list[Expense]) -> int:
        """
        Расчёт всех расходов за период
        """
        tmp = 0
        for element in data:
            try:
                if (self.end_period_date >=
                        element.expense_date >=
                        self.begin_period_date):
                    try:
                        tmp += int(element.amount)
                    except ValueError as err:
                        tmp += 0
                        print('Ошибка, вызванная значением ', element)
                        print(err)
            except AttributeError as err:
                print(err)
        return int(tmp)
