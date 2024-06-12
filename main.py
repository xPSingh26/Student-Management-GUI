from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton
from  PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        fileMenu = self.menuBar().addMenu("&File")
        helpMenu = self.menuBar().addMenu("&Help")
        fileMenuAction = QAction("Add Student", self)
        fileMenuAction.triggered.connect(self.insert_dialog)
        fileMenu.addAction(fileMenuAction)
        helpMenuAction = QAction("About", self)
        helpMenu.addAction(helpMenuAction)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("id", "name", "course", "mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)

        for rowNumber, rowData in enumerate(result):
            self.table.insertRow(rowNumber)
            for columnNumber, data in enumerate(rowData):
                self.table.setItem(rowNumber, columnNumber, QTableWidgetItem(str(data)))

        connection.close()

    def insert_dialog(self):
        dialog = InsertDialogue()
        dialog.exec()


class InsertDialogue(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()

        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setPlaceholderText("Name")
        layout.addWidget(self.nameLineEdit)
        self.courseBox = QComboBox()
        courses = ["Astronomy", "Biology", "Math", "Physics"]
        self.courseBox.addItems(courses)
        layout.addWidget(self.courseBox)
        self.mobileLineEdit = QLineEdit()
        self.mobileLineEdit.setPlaceholderText("Mobile")
        layout.addWidget(self.mobileLineEdit)
        submitButton = QPushButton("Submit")
        submitButton.clicked.connect(self.insert)
        layout.addWidget(submitButton)

        self.setLayout(layout)

    def insert(self):
        name = self.nameLineEdit.text()
        course = self.courseBox.currentText()
        mobile = int(self.mobileLineEdit.text())
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        connection.close()
        appWindow.load_data()


app = QApplication(sys.argv)
appWindow = MainWindow()
appWindow.show()
sys.exit(app.exec())
