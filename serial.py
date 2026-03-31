import serial
import time

ser = serial.Serial('COM3', 9600)

time.sleep(2)

def getTemperatureHumidity(cin):
    try:
        if cin == "T":
            ser.write(b'T')
        elif cin == "B":
            ser.write(b'B')
        elif cin == "S":
            ser.write(b'S')
        elif cin == "H":
            ser.write(b'H')
        elif cin == "C":
            ser.write(b'C')
            raw = input("Hex bytes (ex: 01 03 00 00 00 01): ").strip()
            ser.write((raw + '\n').encode())
        else:
            print("Entrada inválida. Use T', 'B', 'S', 'H' ou 'C'.")

        time.sleep(0.6)
        
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
        else:
            print("Sem resposta")

    except KeyboardInterrupt:
        print("\nEncerrando...")

    finally:
        ser.close()