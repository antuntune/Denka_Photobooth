import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import uic, QtGui

class CustomWidgetPopup(QDialog):
    def __init__(self):
        super().__init__()

        # Load the UI file using loadUi
        uic.loadUi(os.getcwd() + "/res/ui/"+"denka"+"/keyboard.ui", self)  # Replace "widget.ui" with your UI file name

        self.pushButton_enter.clicked.connect(self.close)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.popup_button.clicked.connect(self.show_custom_widget_popup)

    def show_custom_widget_popup(self):
        custom_widget_popup = CustomWidgetPopup()
        custom_widget_popup.setWindowModality(Qt.ApplicationModal)
        custom_widget_popup.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
