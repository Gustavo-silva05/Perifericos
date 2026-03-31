import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from serial import getTemperatureHumidity


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interface.ui", self)
        self.UiComponents()
        self.show()

    def UiComponents(self):
        self.pb_serial = self.findChild(QPushButton, "pb_serial")
        self.pb_cancel = self.findChild(QPushButton, "pb_cancel")
        self.pb_hum = self.findChild(QPushButton, "pb_hum")
        self.pb_send = self.findChild(QPushButton, "pb_send")
        self.pb_temp = self.findChild(QPushButton, "pb_temp")
        self.pb_tempHum = self.findChild(QPushButton, "pb_tempHum")

        self.baudarate_l = self.findChild(QLabel,"baudarate_l")
        self.hum_l = self.findChild(QLabel,"hum_l")
        self.command_l = self.findChild(QLabel,"command_l")
        self.temp_l = self.findChild(QLabel,"temp_l")

        self.command_input = self.findChild(QLineEdit, "command_input")

        self.progressBar = self.findChild(QProgressBar, "progressBar")
        
        self.radioButton = self.findChild(QRadioButton, "radioButton")
        self.radioButton_2 = self.findChild(QRadioButton, "radioButton_2")
        self.radioButton_3 = self.findChild(QRadioButton, "radioButton_3")
        self.radioButton_4 = self.findChild(QRadioButton, "radioButton_4")

        self.temp_lcd = self.findChild(QLCDNumber, "temp_lcd")

        self.pb_serial.clicked.connect()
        self.pb_cancel.clicked.connect(getTemperatureHumidity("C"))
        self.pb_hum.clicked.connect()
        self.pb_send.clicked.connect()
        self.pb_temp.clicked.connect()
        self.pb_tempHum.clicked.connect()

        self.command_input.valueChanged.connect()
        self.radioButton.clicked.connect()
        self.radioButton_2.clicked.connect()
        self.radioButton_3.clicked.connect()
        self.radioButton_4.clicked.connect()


app = QApplication(sys.argv)
window = Window()
app.exec_()
