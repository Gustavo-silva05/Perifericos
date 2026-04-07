import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

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
        
        if res in ["Sem resposta", "Sem conexão"] or "Erro" in res:
            print(f"Falha: {res}")
            return
        
        print(f'resposta: {res}')
        try:
            if cmd == "S":
                self.started = not self.started
                self.pb_serial.setText("Parar Comunicação" if self.started else "Iniciar Comunicação")
            
            elif not self.started:
                print("Inicie a comunicação primeiro (Botão S)")
                return

            elif cmd == "T":
                
                valor = float(res[2:]) if len(res) > 2 else float(res)
                self.temp_lcd.display(valor)
                
            elif cmd == "H":
                valor = int(float(res[2:]))
                self.progressBar.setValue(valor)
                
            elif cmd == "D":
                dados = res.split(':')
                self.temp_lcd.display(float(dados[1]))
                self.progressBar.setValue(int(float(dados[3])))
                
            self.command_l.setText(f"Último: {res}")
            
        except (ValueError, IndexError) as e:
            print(f"Erro ao processar resposta '{res}': {e}")

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
