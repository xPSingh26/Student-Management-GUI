from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QToolBar, QStatusBar
from  PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(600, 400)

        # Create menu bar
        fileMenu = self.menuBar().addMenu("&File")
        helpMenu = self.menuBar().addMenu("&Help")
        editMenu = self.menuBar().addMenu("&Edit")
        fileMenuAction = QAction(QIcon("icons/add.png"), "Add Student", self)
        fileMenuAction.triggered.connect(self.insert_dialog)
        fileMenu.addAction(fileMenuAction)
        helpMenuAction = QAction("About", self)
        helpMenu.addAction(helpMenuAction)
        editMenuAction = QAction(QIcon("icons/search.png"), "Search", self)
        editMenuAction.triggered.connect(self.search_dialog)
        editMenu.addAction(editMenuAction)

        # create tool bar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(fileMenuAction)
        toolbar.addAction(editMenuAction)

        # create table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("id", "name", "course", "mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.load_data()  # load the table contents from database

        # create statusbar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        # detect when cell is clicked
        self.table.cellClicked.connect(self.clicked)

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
        dialog = InsertDialog()
        dialog.exec()

    def search_dialog(self):
        """open the dialog window for search"""
        dialog = SearchDialog()
        dialog.exec()

    def clicked(self):
        editButton = QPushButton("Edit Record")
        editButton.clicked.connect(self.edit_dialog)
        deleteButton = QPushButton("Delete Record")
        deleteButton.clicked.connect(self.delete_dialog)

        # delete existing status bar buttons
        existingButtons = self.findChildren(QPushButton)
        if existingButtons:
            for existingButton in existingButtons:
                self.statusbar.removeWidget(existingButton)

        self.statusbar.addWidget(editButton)
        self.statusbar.addWidget(deleteButton)

    def edit_dialog(self):
        dialog = EditDialog()
        dialog.exec()

    def delete_dialog(self):
        dialog = DeleteDialog()
        dialog.exec()


class InsertDialog(QDialog):
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


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()

        # grab the name from the selected row
        index = appWindow.table.currentRow()
        name = appWindow.table.item(index, 1).text()
        self.nameLineEdit = QLineEdit(name)
        self.nameLineEdit.setPlaceholderText("Name")
        layout.addWidget(self.nameLineEdit)

        # grab the course name from the selected row
        courseName = appWindow.table.item(index, 2).text()
        self.courseBox = QComboBox()
        courses = ["Astronomy", "Biology", "Math", "Physics"]
        self.courseBox.addItems(courses)
        self.courseBox.setCurrentText(courseName)  # set the current item in the list
        layout.addWidget(self.courseBox)

        # grab the mobile number from the current row
        mobile = appWindow.table.item(index, 3).text()
        self.mobileLineEdit = QLineEdit(mobile)
        self.mobileLineEdit.setPlaceholderText("Mobile")
        layout.addWidget(self.mobileLineEdit)

        updateButton = QPushButton("Update")
        updateButton.clicked.connect(self.update)
        layout.addWidget(updateButton)

        self.setLayout(layout)

        def update(self):
            """insert row into the database"""
            pass
            # name = self.nameLineEdit.text()
            # course = self.courseBox.currentText()
            # mobile = int(self.mobileLineEdit.text())
            # connection = sqlite3.connect("database.db")
            # cursor = connection.cursor()
            # cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
            #                (name, course, mobile))
            # connection.commit()
            # connection.close()
            # appWindow.load_data()


class DeleteDialog(QDialog):
    pass


# call code for running the program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    appWindow = MainWindow()
    appWindow.show()
    sys.exit(app.exec())
