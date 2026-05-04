import serial
import time
import sys

port = 'COM4' if sys.platform.startswith('win') else '/dev/ttyUSB0'

try:
    ser = serial.Serial(port, 9600, timeout=1)
    time.sleep(2) 
except Exception as e:
    print(f"Erro ao abrir porta {port}: {e}")
    ser = None

def send_and_receive(cmd, delay=0.4): 
    if not ser: return "Erro: Porta Fechada"
    ser.write(cmd)
    time.sleep(delay)
    if ser.in_waiting > 0:
        try:
            return ser.readline().decode('utf-8').strip()
        except:
            return "Erro de Decode"
    return "Sem resposta"

def serial_communication(cmd, baudrate=9600, data=None):
    if not ser: return "Sem conexão"
    ser.reset_input_buffer() 
    ser.reset_output_buffer()
    try:
        if cmd == "S":
            res = send_and_receive(b'S')
            return "Comunicação iniciada." if "OK" in res else f"Resposta: {res}"
        
        elif cmd in ["T", "H", "D"]:
            return send_and_receive(cmd.encode())
            
        elif cmd == "C":
            ser.reset_input_buffer()
            ser.write(f'C{data}\n'.encode())
            time.sleep(1.0)
            return ser.readline().decode('utf-8').strip() if ser.in_waiting > 0 else "Sem resposta"
            
        elif cmd == "B":
            ser.write(f'B{baudrate}\n'.encode())
            time.sleep(0.2)
            response = ser.readline().decode('utf-8').strip()
            ser.baudrate = int(baudrate) 
            return response
            
        return "Comando inválido"
    except Exception as e:
        return f"Erro: {str(e)}"
