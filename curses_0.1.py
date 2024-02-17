import serial
import ast
import re  # Для работы с регулярными выражениями
import curses
import time

# Создаем объект для работы с последовательным портом
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)


def display_data_curses(stdscr):
    curses.curs_set(0)  # Скрываем курсор
    stdscr.nodelay(True)  # Установка неблокирующего режима для чтения клавиш

    while True:
        if ser.in_waiting > 0:
            incoming_data = ser.readline().decode('utf-8').rstrip()
            process_incoming_data(stdscr, incoming_data)
        # Добавляем небольшую задержку для уменьшения нагрузки на процессор
        time.sleep(0.008) #работает от 0.01 и меньше


def process_incoming_data(stdscr, data):
    try:
        match = re.search(r"array\('H', (\[.*?\])\)", data)
        if match:
            data_str = match.group(1)
            channels = ast.literal_eval(data_str)
            if isinstance(channels, list):
                display_channels(stdscr, channels)
    except ValueError as e:
        stdscr.addstr(0, 0, "Error parsing incoming data")
        stdscr.refresh()


def display_channels(stdscr, channels):
    for i, value in enumerate(channels, start=1):
        stdscr.move(i - 1, 0)  # Перемещаем курсор на начало строки
        stdscr.clrtoeol()  # Очищаем строку
        stdscr.addstr(i - 1, 0, f"Channel {i}: {value}    ")
    stdscr.refresh()  # Обновляем экран


if __name__ == "__main__":
    curses.wrapper(display_data_curses)
