from bookkeeper.view.GUI import GUI
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from PySide6 import QtWidgets
from bookkeeper.utils import read_tree
import sys

exp_repo_sql = SQLiteRepository[Expense]('database.db', Expense)
cat_repo_sql = SQLiteRepository[Category]('database.db', Category)
cat_repo_sql.delete_all()

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

Category.create_from_tree(read_tree(cats), cat_repo_sql)

app = QtWidgets.QApplication(sys.argv)
window = GUI(exp_repo_sql, cat_repo_sql)
window.show()
app.exec()
