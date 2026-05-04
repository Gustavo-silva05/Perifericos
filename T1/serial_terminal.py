import serial
import time

ser = serial.Serial('COM3', 9600)
ser.timeout = 3.0
time.sleep(2)
ser.reset_input_buffer()

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
            cin = input("Digite (T/H/D/B/C/S): ").strip().upper()

            if cin == "S":
                response = send_and_receive(b'S')
                print("Comunicação encerrada.")
                break  

            elif cin == "T":
                print(send_and_receive(b'T'))
            elif cin == "H":
                print(send_and_receive(b'H'))
            elif cin == "D":
                print(send_and_receive(b'D'))
            elif cin == "C":
                raw = input("Hex bytes (ex: 01 03 00 00 00 01): ").strip()
                ser.write(('C' + raw + '\n').encode())
                line = ser.readline().decode('utf-8').rstrip()
                print(line if line else "Sem resposta")
                ser.reset_input_buffer()
            elif cin == "B":
                raw = input("Novo baudrate (ex: 115200): ").strip()
                ser.write(('B' + raw + '\n').encode())
                line = ser.readline().decode('utf-8').rstrip()
                if line == "OK":
                    print("Baudrate atualizado.")
                else:
                    print(f"Resposta inesperada: {line}")
                ser.baudrate = int(raw)
                time.sleep(0.5)
                ser.reset_input_buffer()
                
            else:
                print("Entrada inválida. Use (T/H/D/B/C/S).")

except KeyboardInterrupt:
    print("\nEncerrando...")

finally:
    ser.close()
