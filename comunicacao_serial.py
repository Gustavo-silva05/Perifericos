import serial
import time
import sys

if sys.platform.startswith('win'):
    port = 'COM3'
else:
    port = '/dev/ttyUSB0'

ser = serial.Serial(port, 9600)
time.sleep(2)

def send_and_receive(cmd, delay=0.6):
    ser.write(cmd)
    time.sleep(delay)
    if ser.in_waiting > 0:
        return ser.readline().decode('utf-8').rstrip()
    return "Sem resposta"

def serial_communication(cmd, baudrate , data=None):
    try:
        if cmd == "S":
            response = send_and_receive(b'S')
            if response == "OK":
                return "Comunicação iniciada."
            else:
                return(f"Resposta inesperada: {response}")

        elif cmd == "T":
            return(send_and_receive(b'T'))
        elif cmd == "H":
            return(send_and_receive(b'H'))
        elif cmd == "TH":
            return(send_and_receive(b'TH'))
        elif cmd == "C":
            ser.reset_input_buffer()
            ser.write(('C' + data + '\n').encode())
            time.sleep(2.0)
            if ser.in_waiting > 0:
                return(ser.readline().decode('utf-8').rstrip())
            else:
                return("Sem resposta")
        elif cmd == "B":
            ser.reset_input_buffer()
            ser.write(('B' + str(baudrate) + '\n').encode())
            time.sleep(0.5)
            if ser.in_waiting > 0:
                return(ser.readline().decode('utf-8').rstrip())
            ser.baudrate = int(baudrate)
        else:
            return("Entrada inválida. Use 'T', 'B', 'H', 'C' ou 'S'.")

    except KeyboardInterrupt:
        print("\nEncerrando...")

    
def close():
    ser.close()
