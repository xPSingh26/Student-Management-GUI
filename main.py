from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton
from  PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        fileMenu = self.menuBar().addMenu("&File")
        helpMenu = self.menuBar().addMenu("&Help")
        editMenu = self.menuBar().addMenu("&Edit")
        fileMenuAction = QAction("Add Student", self)
        fileMenuAction.triggered.connect(self.insert_dialog)
        fileMenu.addAction(fileMenuAction)
        helpMenuAction = QAction("About", self)
        helpMenu.addAction(helpMenuAction)
        editMenuAction = QAction("Search", self)
        editMenuAction.triggered.connect(self.search_dialog)
        editMenu.addAction(editMenuAction)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("id", "name", "course", "mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.load_data()

    def load_data(self):
        """load the database into window table"""
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)

        for rowNumber, rowData in enumerate(result):
            self.table.insertRow(rowNumber)
            for columnNumber, data in enumerate(rowData):
                self.table.setItem(rowNumber, columnNumber, QTableWidgetItem(str(data)))

        connection.close()

    def insert_dialog(self):
        """open the dialog window for add student"""
        dialog = InsertDialogue()
        dialog.exec()

    def search_dialog(self):
        """open the dialog window for search"""
        dialog = SearchDialog()
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
        """insert row into the database"""
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


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search for Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()

        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setPlaceholderText("Enter Name")
        searchButton = QPushButton("Search")
        searchButton.clicked.connect(self.search)
        layout.addWidget(self.nameLineEdit)
        layout.addWidget(searchButton)

        self.setLayout(layout)

    def search(self):
        """search for name in current database and highlight the rows returned"""
        name = self.nameLineEdit.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)
        items = appWindow.table.findItems(name, Qt.MatchFlag.MatchFixedString) # return the rows with the entered name
        for item in items:
            appWindow.table.item(item.row(), 1).setSelected(True) # highlight all the rows with matched name

        cursor.close()
        connection.close()


# call code for running the program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    appWindow = MainWindow()
    appWindow.show()
    sys.exit(app.exec())
