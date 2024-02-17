import serial
import ast
import re  # Для работы с регулярными выражениями
import curses
import time

# Настройка последовательного порта
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)


def display_data_curses(stdscr):
    curses.curs_set(0)  # Скрываем курсор
    stdscr.nodelay(True)  # Неблокирующий режим
    # Не очищаем весь экран на каждой итерации
    while True:
        if ser.in_waiting > 0:
            incoming_data = ser.readline().decode('utf-8').rstrip()
            try:
                match = re.search(r"array\('H', (\[.*?\])\)", incoming_data)
                if match:
                    data_str = match.group(1)
                    channels = ast.literal_eval(data_str)
                    if isinstance(channels, list):
                        for i, value in enumerate(channels, start=1):
                            stdscr.move(i - 1, 0)  # Перемещаем курсор
                            stdscr.clrtoeol()  # Очищаем строку
                            stdscr.addstr(
                                i - 1, 0, f"Channel {i}: {value}    ")
                stdscr.refresh()  # Обновляем экран
            except ValueError as e:
                pass
        time.sleep(0.01)  # Добавляем небольшую задержку


if __name__ == "__main__":
    curses.wrapper(display_data_curses)
