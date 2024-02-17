import serial
import time

# Настройте порт в соответствии с вашей системой. Например, '/dev/ttyACM0'
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.flush()


def main():
    while True:
        ser.write(b"data\r\n")  # Отправляем данные на Pico
        time.sleep(1)  # Пауза для демонстрации
        if ser.in_waiting > 0:
            incoming_data = ser.readline().decode('utf-8').rstrip()  # Читаем ответ от Pico
            print(f"Received: {incoming_data}")


if __name__ == "__main__":
    main()



