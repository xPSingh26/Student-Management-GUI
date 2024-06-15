from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QToolBar, QStatusBar, QGridLayout, QLabel, QMessageBox
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
        try:
            name = self.nameLineEdit.text()
            course = self.courseBox.currentText()
            mobile = self.mobileLineEdit.text()
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                           (name, course, mobile))
            connection.commit()
            connection.close()
            appWindow.load_data()
            self.close()
            confirmation = QMessageBox()
            confirmation.setWindowTitle("Success!")
            confirmation.setText("The record was added successfully!")
            confirmation.exec()
        except ValueError:
            confirmation = QMessageBox()
            confirmation.setWindowTitle("Failed!")
            confirmation.setText("Please enter all details! ")
            confirmation.exec()


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
        connection = connect()
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)
        items = appWindow.table.findItems(name, Qt.MatchFlag.MatchFixedString)  # return the rows with the entered name
        for item in items:
            appWindow.table.item(item.row(), 1).setSelected(True) # highlight all the rows with matched name

        cursor.close()
        connection.close()
        self.close()


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

        # grab the id of current row
        self.id = appWindow.table.item(index, 0).text()

        updateButton = QPushButton("Update")
        updateButton.clicked.connect(self.update)
        layout.addWidget(updateButton)

        self.setLayout(layout)

    def update(self):
        """update selected row into the database"""
        try:
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                           (self.nameLineEdit.text(), self.courseBox.currentText(), self.mobileLineEdit.text(), self.id))
            connection.commit()
            cursor.close()
            connection.close()
            appWindow.load_data()
            self.close()
            confirmation = QMessageBox()
            confirmation.setWindowTitle("Success!")
            confirmation.setText("The record was edited successfully!")
            confirmation.exec()
        except ValueError:
            confirmation = QMessageBox()
            confirmation.setWindowTitle("Failed!")
            confirmation.setText("Please enter all details! ")
            confirmation.exec()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Data")
        layout = QGridLayout()

        label = QLabel("Are you sure you want to delete this record?")
        yesButton = QPushButton("Yes")
        noButton = QPushButton("No")
        yesButton.clicked.connect(self.delete)
        noButton.clicked.connect(self.close)
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(yesButton, 1, 0)
        layout.addWidget(noButton, 1, 1)
        self.setLayout(layout)

        # grab the id of selected row
        index = appWindow.table.currentRow()
        self.id = appWindow.table.item(index, 0).text()

    def delete(self):
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (self.id, ))
        connection.commit()
        cursor.close()
        connection.close()
        appWindow.load_data()
        self.close()
        confirmation = QMessageBox()
        confirmation.setWindowTitle("Success!")
        confirmation.setText("The record was deleted successfully!")
        confirmation.exec()


def connect(database_path="database.db"):
    connection = sqlite3.connect(database_path)
    return connection


# call code for running the program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    appWindow = MainWindow()
    appWindow.show()
    sys.exit(app.exec())
