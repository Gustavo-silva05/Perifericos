#include <Arduino.h>

#define MAX485_DE_RE 2

// slide 12 do MODBUS indica essas portas

#define REG_TEMP 0x0001
#define REG_HUMI 0x0002

#define BAUDRATE 9600

// funcoes para comm MODBUS
void sendModbus(unsigned char *frame, int len);
bool receiveModbus(int expectedBytes);

// funcoes do sor, print para debug
void printHexMessage(unsigned char values[], int tamanho);
void printHexByte(unsigned char b);
void calculateCRC(unsigned char *frame, int tamanho);

// criando o frame de 8 bytes
void buildFrame(unsigned char *frame, uint16_t startReg, uint16_t quantity);

// printando os valores em string
void printTemp();
void printHumi();
void printTempAndHumi();

// recebe um comando qualquer
void receiveCommand(String hexInput);

int TIMEOUT = 500;

unsigned char crc_saida[2];
unsigned char msg_rx[9];
unsigned char tx_frame[8];

void setup() {
    Serial.begin(BAUDRATE);                       // baudrate1 (PC -> ESP32)
    Serial1.begin(BAUDRATE, SERIAL_8N1, 16, 17);  // baudrate2 (ESP32 -> MODBUS)
    pinMode(MAX485_DE_RE, OUTPUT);
    digitalWrite(MAX485_DE_RE, LOW);
    delay(1000);
}

void loop() {
    if (Serial.available()) {
        char cmd = Serial.read();

        if (cmd == 'S') {
            Serial.println("OK");

        } else if (cmd == 'T') {
            buildFrame(tx_frame, REG_TEMP, 1);
            sendModbus(tx_frame, 8);
            if (receiveModbus(7)) printTemp();
            else Serial.println("ERR");

        } else if (cmd == 'H') {
            buildFrame(tx_frame, REG_HUMI, 1);
            sendModbus(tx_frame, 8);
            if (receiveModbus(7)) printHumi();
            else Serial.println("ERR");

        } else if (cmd == 'TH') {
            buildFrame(tx_frame, REG_TEMP, 2);
            sendModbus(tx_frame, 8);
            if (receiveModbus(9)) printTempAndHumi();
            else Serial.println("ERR");

        } else if (cmd == 'C') {
            String raw = Serial.readStringUntil('\n');
            receiveCommand(raw);
        } else if (cmd == 'B') {
            String raw = Serial.readStringUntil('\n');
            int newBaudrate = raw.toInt();
            Serial.println("OK");
            delay(100); 
            Serial.end();
            Serial.begin(newBaudrate);
        }
    }
}

// Funções para imprimir os bytes enviados na Serial0.

void printHexMessage(unsigned char values[], int tamanho) {
  for (int i = 0; i < tamanho; i++) {
    printHexByte(values[i]);
  }
  Serial.println();
}

void printHexByte(unsigned char b)
{
  Serial.print((b >> 4) & 0xF, HEX);
  Serial.print(b & 0xF, HEX);
  Serial.print(' ');
}

void calculateCRC(unsigned char *frame, int tamanho) {
  unsigned int crc = 0xFFFF;            // Initialize CRC to 0xFFFF
  for (int n = 0; n < tamanho; n++) {
    crc ^= frame[n];                    // XOR the frame byte with the CRC
    for (int m = 0; m < 8; m++) {
      if (crc & 0x0001) {               // Check if the LSB of the CRC is 1
        crc >>= 1;                      // Right shift the CRC
        crc ^= 0xA001;                  // XOR the CRC with the polynomial 0xA001
      } else {
        crc >>= 1;                      // Right shift the CRC
      }
    }
  }
  crc_saida[1] = (crc >> 8) & 0xFF;     // Separando a parte alta do CRC  
  crc_saida[0] = crc & 0xFF;
}

// criando funcoes com a logica do sor de escrever e ler a serial1 (MODBUS)

void sendModbus(unsigned char *frame, int len) { 
    digitalWrite(MAX485_DE_RE, HIGH);
    delay(10);
    Serial1.write(frame, len);
    Serial1.flush();
    digitalWrite(MAX485_DE_RE, LOW);
}

bool receiveModbus(int expectedBytes) { 
    uint32_t startTime = millis();
    int j = 0;

    while (millis() - startTime <= TIMEOUT) {
        if (Serial1.available()) {
            msg_rx[j] = Serial1.read();
            j++;
            if (j >= expectedBytes) break;  
        }
    }

    return (j == expectedBytes);  
}

// slide 13, 14 e 15 do MODBUS
void buildFrame(unsigned char *frame, uint16_t startReg, uint16_t quantity) {
    frame[0] = 0x01;                    // Device Address
    frame[1] = 0x04;                    // function code (Read)
    frame[2] = (startReg >> 8) & 0xFF;  // Starting Address Hi
    frame[3] = startReg & 0xFF;         // Starting Address Li
    frame[4] = (quantity >> 8) & 0xFF;  // Quantity Hi
    frame[5] = quantity & 0xFF;         // Quantity Li
    calculateCRC(frame, 6);             // para calcular o CRC
    frame[6] = crc_saida[0];            // CRC Hi
    frame[7] = crc_saida[1];            // CRC Li
}

// nao sei como que o sensor retorna temperatura e humidade,
// mas imagino que seja 20.5C = msg[3] = 20 e msg[4] = 5,
// entao faz um concat bitwise e depois divide por 10

// estrutura do msg_rx tambem nos slides 13, 14 e 15
void printTemp() { 
    int16_t rawTemp = (msg_rx[3] << 8) | msg_rx[4];
    float temp = rawTemp / 10.0;
    Serial.print("T:");
    Serial.println(temp);
}

void printHumi() {
    int16_t rawHum = (msg_rx[3] << 8) | msg_rx[4];
    float humi = rawHum / 10.0;
    Serial.print("H:");
    Serial.println(humi);
}

void printTempAndHumi() {
    int16_t rawTemp = (msg_rx[3] << 8) | msg_rx[4];
    int16_t rawHum  = (msg_rx[5] << 8) | msg_rx[6];
    float temp = rawTemp / 10.0;
    float humi = rawHum / 10.0;
    Serial.print("T:");
    Serial.print(temp);
    Serial.print(":H:");
    Serial.println(humi);
}

// recebe um comando tipo 01 02 03 04 05 06 e manda pro sensor
void receiveCommand(String input) {
    unsigned char frame[10];
    int len = 0;

    // divide os espacos em bytes
    int start = 0;
    for (int i = 0; i <= input.length(); i++) {
        if (input[i] == ' ' || i == input.length()) {
            String byteStr = input.substring(start, i); // pega o ultimo byte
            if (byteStr.length() > 0) {
                frame[len++] = (unsigned char) strtol(byteStr.c_str(), NULL, 16); // converte a string pra numero
            }
            start = i + 1;
        }
    }

    calculateCRC(frame, len);
    frame[len++] = crc_saida[0];
    frame[len++] = crc_saida[1];

    sendModbus(frame, len);

    // nao tem como saber o tamanho da resposta do sensor
    // entao usa timer pra esperar um tempo e boa
    uint32_t startTime = millis();
    int j = 0;
    while (millis() - startTime <= TIMEOUT) {
        if (Serial1.available() && j < sizeof(msg_rx)) {
            msg_rx[j++] = Serial1.read();
        }
    }

    if (j > 0) {
        Serial.print("C:");
        for (int i = 0; i < j; i++) {
            if (msg_rx[i] < 0x10) Serial.print("0");
            Serial.print(msg_rx[i], HEX);
            if (i < j-1) Serial.print(" ");
        }
        Serial.println();
    } else {
        Serial.println("ERR");
    }
}