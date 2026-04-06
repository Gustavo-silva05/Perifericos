import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import random
from comunicacao_serial import serial_communication

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interface.ui", self)
        self.UiComponents()
        self.show()
        self.started =False
        

    def send_command(self, cmd, baudrate=9600, data=None):
        res = serial_communication(cmd, baudrate, data)
        print(f"Comando: {cmd}")
        if cmd == "S":
            if self.started:
                self.started = False
                self.pb_serial.setText("Iniciar Comunicação")
            else:
                self.started = True
                self.pb_serial.setText("Parar Comunicação")
        
        elif not self.started:
            print("Programa não Iniciado")
            return

        elif cmd == "T":
            self.temp_lcd.display((float(res[2:])))
        elif cmd == "H":
            self.progressBar.setValue(int(float(res[2:])))
        elif cmd == "D":
            temp, hum = res[2:].split(',')
            self.temp_lcd.display(int(float(temp)))
            self.progressBar.setValue(int(float(hum)))
        else:
            self.command_l.setText(f"Comando enviado: {cmd}")

    def UiComponents(self):
        self.pb_serial = self.findChild(QPushButton, "pb_serial")
        self.pb_serial.setText("Iniciar Comunicação")
        self.pb_cancel = self.findChild(QPushButton, "pb_cancel")
        self.pb_hum = self.findChild(QPushButton, "pb_hum")
        self.pb_send = self.findChild(QPushButton, "pb_send")
        self.pb_temp = self.findChild(QPushButton, "pb_temp")
        self.pb_tempHum = self.findChild(QPushButton, "pb_tempHum")

        self.hum_l = self.findChild(QLabel,"hum_l")
        self.command_l = self.findChild(QLabel,"command_l")
        self.temp_l = self.findChild(QLabel,"temp_l")
        self.baudrate_l = self.findChild(QLabel,"baudrate_l")

        self.command_line = self.findChild(QLineEdit, "command_line")

        self.progressBar = self.findChild(QProgressBar, "progressBar")
        
        self.radioButton_9600 = self.findChild(QRadioButton, "radioButton_9600")
        self.radioButton_9600.setChecked(True)

        self.radioButton_115200 = self.findChild(QRadioButton, "radioButton_115200")
        self.radioButton_921600 = self.findChild(QRadioButton, "radioButton_921600")

        self.temp_lcd = self.findChild(QLCDNumber, "temp_lcd")

        self.pb_cancel.clicked.connect(lambda: self.command_line.clear())
        self.pb_serial.clicked.connect(lambda: self.send_command("S"))
        self.pb_hum.clicked.connect(lambda: self.send_command("H"))
        self.pb_send.clicked.connect(lambda: self.send_command("C", None ,self.command_line.text()))
        self.pb_temp.clicked.connect(lambda: self.send_command("T"))
        self.pb_tempHum.clicked.connect(lambda: self.send_command("D"))

        self.radioButton_9600.clicked.connect(lambda: self.send_command("B",9600))
        self.radioButton_115200.clicked.connect(lambda: self.send_command("B",115200))
        self.radioButton_921600.clicked.connect(lambda: self.send_command("B",921600))

app = QApplication(sys.argv)
window = Window()
with open("style.css", "r") as f:
    app.setStyleSheet(f.read())
app.exec_()
