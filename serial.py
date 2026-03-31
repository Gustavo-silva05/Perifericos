import serial
import time

ser = serial.Serial('COM3', 9600)
time.sleep(2)

def send_and_receive(cmd, delay=0.6):
    ser.write(cmd)
    time.sleep(delay)
    if ser.in_waiting > 0:
        return ser.readline().decode('utf-8').rstrip()
    return "Sem resposta"

try:
    while True:
        print("Digite S para iniciar a comunicação.")
        while True:
            cin = input("Digite (S): ").strip().upper()
            if cin == "S":
                response = send_and_receive(b'S')
                if response == "OK":
                    print("Comunicação iniciada.")
                    break
                else:
                    print(f"Resposta inesperada: {response}")
            else:
                print("Digite 'S' para iniciar.")

        while True:
            cin = input("Digite (T/H/TH/B/C/S): ").strip().upper()

            if cin == "S":
                response = send_and_receive(b'S')
                print("Comunicação encerrada.")
                break  

            elif cin == "T":
                print(send_and_receive(b'T'))
            elif cin == "H":
                print(send_and_receive(b'H'))
            elif cin == "TH":
                print(send_and_receive(b'TH'))
            elif cin == "C":
                ser.write(b'C')
                raw = input("Hex bytes (ex: 01 03 00 00 00 01): ").strip()
                ser.write((raw + '\n').encode())
                time.sleep(2.0)
                if ser.in_waiting > 0:
                    print(ser.readline().decode('utf-8').rstrip())
                else:
                    print("Sem resposta")
            elif cin == "B":
                raw = input("Novo baudrate (ex: 115200): ").strip()
                ser.write(b'B')
                ser.write((raw + '\n').encode())
                time.sleep(0.5)
                if ser.in_waiting > 0:
                    print(ser.readline().decode('utf-8').rstrip())
                ser.baudrate = newBaudrate
            else:
                print("Entrada inválida. Use 'T', 'B', 'H', 'C' ou 'S'.")

except KeyboardInterrupt:
    print("\nEncerrando...")

finally:
    ser.close()