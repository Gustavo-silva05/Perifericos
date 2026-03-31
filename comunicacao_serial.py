import serial
import time
import sys

if sys.platform.startswith('win'):
    port = 'COM3'
else:
    port = '/dev/ttyUSB0'

ser = serial.Serial(port, 9600)
time.sleep(2)
start = False

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
            start = not start
            if response == "OK":
                print("Comunicação iniciada.")
            else:
                print(f"Resposta inesperada: {response}")

        elif cmd == "T":
            print(send_and_receive(b'T'))
        elif cmd == "H":
            print(send_and_receive(b'H'))
        elif cmd == "TH":
            print(send_and_receive(b'TH'))
        elif cmd == "C":
            ser.write(b'C')
            raw = input("Hex bytes (ex: 01 03 00 00 00 01): ").strip()
            ser.write((raw + '\n').encode())
            time.sleep(2.0)
            if ser.in_waiting > 0:
                print(ser.readline().decode('utf-8').rstrip())
            else:
                print("Sem resposta")
        elif cmd == "B":
            ser.write(b'B')
            ser.write((baudrate + '\n').encode())
            time.sleep(0.5)
            if ser.in_waiting > 0:
                print(ser.readline().decode('utf-8').rstrip())
            ser.baudrate = int(baudrate)
        else:
            print("Entrada inválida. Use 'T', 'B', 'H', 'C' ou 'S'.")

    except KeyboardInterrupt:
        print("\nEncerrando...")

    finally:
        ser.close()