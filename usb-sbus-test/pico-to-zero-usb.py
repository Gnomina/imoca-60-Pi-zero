
import select
import sys
import machine
import time

# Настройка светодиода
led = machine.Pin(25, machine.Pin.OUT)

# Функция для мигания светодиодом


def blink_led(times, speed):
    for _ in range(times):
        led.value(1)
        time.sleep(speed)
        led.value(0)
        time.sleep(speed)


# Set up the poll object
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

# Loop indefinitely
while True:
    # Ожидание входных данных
    # Увеличено время ожидания до 100 микросекунд
    poll_results = poll_obj.poll(100)
    if poll_results:
        # Чтение данных из stdin (данные, полученные от Zero)
        data = sys.stdin.readline().strip()
        # Вывод полученных данных
        sys.stdout.write("received data: " + data + "\r\n")
        # Мигание светодиодом 4 раза быстро при получении данных
        blink_led(4, 0.05)
    else:
        # Мигание светодиодом 2 раза быстро, когда ожидает данные
        blink_led(2, 0.1)



