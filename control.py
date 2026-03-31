import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import random
# from comunicacao_serial import serial_communication

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.baudrate = None  # Declarado antes de usar
        uic.loadUi("interface.ui", self)
        self.UiComponents()
        self.show()

    def set_baudrate(self, value):
        self.baudrate_l.setText(f'Baudrate: {value} bps')
        self.baudrate = value

    def send_command(self, cmd):
        # res = serial_communication(cmd, self.baudrate)
        hum = random.randint(0, 100)
        temp = round(random.uniform(0.0, 40.0))
        resT = f'T:{temp}'
        resH = "H:" + str(hum)
        resTH = "TH:" + str(temp) + "," + str(hum)
        print(f"Comando: {cmd}, Baudrate: {self.baudrate}")
        if cmd == "S":
            if self.pb_serial.text() == "Iniciar Comunicação":
                self.pb_serial.setText("Parar Comunicação")
            else:
                self.pb_serial.setText("Iniciar Comunicação")
        elif cmd == "T":
            self.temp_lcd.display(int(resT[2:]))
        elif cmd == "H":
            self.progressBar.setValue(int(resH[2:]))
        elif cmd == "TH":
            temp, hum = resTH[3:].split(',')
            self.temp_lcd.display(int(temp))
            self.progressBar.setValue(int(hum))
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
        self.set_baudrate(9600)

        self.radioButton_115200 = self.findChild(QRadioButton, "radioButton_115200")
        self.radioButton_921600 = self.findChild(QRadioButton, "radioButton_921600")

        self.temp_lcd = self.findChild(QLCDNumber, "temp_lcd")

        self.pb_cancel.clicked.connect(lambda: self.command_line.clear())
        self.pb_serial.clicked.connect(lambda: self.send_command("S"))
        self.pb_hum.clicked.connect(lambda: self.send_command("H"))
        self.pb_send.clicked.connect(lambda: self.send_command(self.command_line.text()))
        self.pb_temp.clicked.connect(lambda: self.send_command("T"))
        self.pb_tempHum.clicked.connect(lambda: self.send_command("TH"))

        self.radioButton_9600.clicked.connect(lambda: self.set_baudrate(9600))
        self.radioButton_115200.clicked.connect(lambda: self.set_baudrate(115200))
        self.radioButton_921600.clicked.connect(lambda: self.set_baudrate(921600))

app = QApplication(sys.argv)
window = Window()
with open("style.css", "r") as f:
    app.setStyleSheet(f.read())
app.exec_()