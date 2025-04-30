from PySide6.QtWidgets import QApplication
from user_class import  Connect
from main_window import MainW

app = QApplication([])
session = Connect.con()
window = MainW(session)
window.show()
app.exec()