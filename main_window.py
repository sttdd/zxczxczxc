from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QWidget, QTableWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, \
    QLabel, QPushButton, QTableWidgetItem, QMessageBox, QDialog, QFormLayout
from sqlalchemy.orm import Session

from user_class import Employee, Company


class MainW(QMainWindow):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        self.setWindowTitle("qwe")
        self.setWindowIcon(QIcon("logo.png"))
        self.main_ui()
        self.pop_t()
        self.pop_com()

    def main_ui(self):
        cw = QWidget()
        self.setCentralWidget(cw)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["id","name","date","company"])
        ml = QVBoxLayout(cw)
        ml.addWidget(self.table)

        fl = QHBoxLayout()
        self.name_i = QLineEdit()
        self.name_i.setPlaceholderText("поиск по имени")
        self.name_i.textChanged.connect(self.ft)
        self.comp_i = QComboBox()
        self.comp_i.addItem("все компании")
        self.comp_i.currentTextChanged.connect(self.ft)

        fl.addWidget(QLabel("поиск"))
        fl.addWidget(self.name_i)
        fl.addWidget(QLabel("компании"))
        fl.addWidget(self.comp_i)
        ml.addLayout(fl)

        bl = QHBoxLayout()
        add_b = QPushButton("add")
        dell_b = QPushButton("dell")
        bl.addWidget(add_b)
        bl.addWidget(dell_b)
        add_b.clicked.connect(self.add_e)
        dell_b.clicked.connect(self.dell_e)
        ml.addLayout(bl)

    def pop_t(self):
        empl = self.session.query(Employee).all()
        self.table.setRowCount(len(empl))
        for row, emp in enumerate(empl):
            self.table.setItem(row, 0, QTableWidgetItem(str(emp.id)))
            self.table.setItem(row, 1, QTableWidgetItem(emp.name))
            self.table.setItem(row, 2, QTableWidgetItem(emp.data))
            self.table.setItem(row, 3, QTableWidgetItem(emp.company.name))

    def pop_com(self):
        comp = self.session.query(Company).all()
        self.comp_i.clear()
        self.comp_i.addItem("все компании")
        self.comp_i.addItems([com.name for com in comp])

    def ft(self):
        name = self.name_i.text().lower()
        comp = self.comp_i.currentText()
        query = self.session.query(Employee)
        if name:
            query = query.filter(Employee.name.ilike(f"%{name}%"))
        if comp != "все компании":
            query = query.join(Company).filter(Company.name == comp)

        empl = query.all()
        self.table.setRowCount(len(empl))
        for row, emp in enumerate(empl):
            self.table.setItem(row, 0, QTableWidgetItem(str(emp.id)))
            self.table.setItem(row, 1, QTableWidgetItem(emp.name))
            self.table.setItem(row, 2, QTableWidgetItem(emp.data))
            self.table.setItem(row, 3, QTableWidgetItem(emp.company.name))

    def dell_e(self):
        ses = self.table.currentRow()
        if ses>=0:
            emp_id = int(self.table.item(ses, 0).text())
            emp = self.session.query(Employee).filter_by(id = emp_id).first()
            if emp:
                name = emp.name
                surname = emp.surname
                self.session.delete(emp)
                self.session.commit()
                self.pop_t()
                QMessageBox.information(self, "del", f"{name} {surname} del")

    def add_e(self):
        d = AddE(self.session, self)
        if d.exec():
            self.pop_t()
            self.pop_com()

class AddE(QDialog):
    def __init__(self, session: Session, t=None):
        super().__init__(t)
        self.session = session
        self.setWindowTitle("add")
        self.add_ui()

    def add_ui(self):
        l = QFormLayout(self)
        self.name = QLineEdit()
        self.surname = QLineEdit()
        self.s_pas = QLineEdit()
        self.n_pas = QLineEdit()
        self.adres = QLineEdit()
        self.data = QLineEdit()
        self.comp_name = QComboBox()

        comp = self.session.query(Company).all()
        self.comp_name.addItems([com.name for com in comp])

        l.addRow("имя",self.name)
        l.addRow("имя", self.surname)
        l.addRow("имя", self.s_pas)
        l.addRow("имя", self.n_pas)
        l.addRow("имя", self.adres)
        l.addRow("имя", self.data)
        l.addRow("имя", self.comp_name)

        bl = QHBoxLayout()
        add_b = QPushButton("ADD")
        cancel_b = QPushButton("cancel")
        bl.addWidget(add_b)
        bl.addWidget(cancel_b)
        cancel_b.clicked.connect(self.reject)
        add_b.clicked.connect(self.add_e)
        l.addRow(bl)

    def add_e(self):
        name = self.name.text()
        surname = self.surname.text()
        s_pas = self.s_pas.text()
        n_pas = self.n_pas.text()
        adres = self.adres.text()
        data = self.data.text()
        comp_name = self.comp_name.currentText()

        if not all([name,surname,s_pas,n_pas,adres,data,comp_name]):
            QMessageBox.information(self, "w!", "заполните все поля!")
            return

        comp = self.session.query(Company).filter_by(name = comp_name).first()
        if comp:
            emp = Employee(
                name = name,
                surname = surname,
                s_pas = s_pas,
                n_pas = n_pas,
                adres = adres,
                data = data,
                company = comp
            )
            self.session.add(emp)
            self.session.commit()
            self.accept()