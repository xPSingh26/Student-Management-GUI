from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidget
from  PyQt6.QtGui import QAction
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        fileMenu = self.menuBar().addMenu("&File")
        helpMenu = self.menuBar().addMenu("&Help")
        fileMenuAction = QAction("Add Student", self)
        fileMenu.addAction(fileMenuAction)
        helpMenuAction = QAction("About", self)
        helpMenu.addAction(helpMenuAction)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("id", "name", "course", "mobile"))
        self.setCentralWidget(self.table)


app = QApplication(sys.argv)
appWindow = MainWindow()
appWindow.show()
sys.exit(app.exec())
