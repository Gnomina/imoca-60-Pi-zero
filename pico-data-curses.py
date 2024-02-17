import serial
import ast
import re  # Для работы с регулярными выражениями
import curses
import time
import subprocess


def get_cpu_temperature():
    process = subprocess.Popen(
        ['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    temperature_str = output.decode(
        'utf-8').replace('temp=', '').replace('\'C\n', '')
    return float(temperature_str)


# Создаем объект для работы с последовательным портом
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)


def pico_data():
    if ser.in_waiting > 0:
        incoming_data = ser.readline().decode('utf-8').rstrip()
        match = re.search(r"array\('H', (\[.*?\])\)", incoming_data)
        if match:
            data_str = match.group(1)
            try:
                channels = ast.literal_eval(data_str)
                if isinstance(channels, list):
                    return channels
            except ValueError:
                return None
    return None


def display_data_curses(stdscr):
    curses.curs_set(0)  # Скрываем курсор
    stdscr.nodelay(True)  # Установка неблокирующего режима для чтения клавиш

    prev_channels = []  # Хранение предыдущего состояния каналов для сравнения
    prev_cpu_temp = None  # Хранение предыдущего значения температуры для сравнения

    update_interval_channels = 0.008  # Интервал обновления для каналов
    update_interval_temperature = 1.0  # Интервал обновления для температуры CPU

    last_update_time_channels = time.time()
    last_update_time_temperature = time.time()

    while True:
        current_time = time.time()

        # Обновление каналов в соответствии с их интервалом обновления
        if current_time - last_update_time_channels >= update_interval_channels:
            channels = pico_data()
            if channels is not None and channels != prev_channels:
                for i, value in enumerate(channels, start=1):
                    line = f"Channel {i}: {value}    "
                    stdscr.move(i, 0)
                    stdscr.clrtoeol()  # Очищаем текущую строку перед выводом новых данных
                    stdscr.addstr(i, 0, line)
                prev_channels = channels
            last_update_time_channels = current_time

        # Обновление температуры CPU в соответствии с ее интервалом обновления
        if current_time - last_update_time_temperature >= update_interval_temperature:
            cpu_temperature = get_cpu_temperature()
            if cpu_temperature != prev_cpu_temp:  # Обновляем температуру только при изменении
                # Предполагая, что у вас достаточно места на экране
                stdscr.move(20, 0)
                stdscr.clrtoeol()
                stdscr.addstr(20, 0, f"CPU Temp: {cpu_temperature}°C")
                prev_cpu_temp = cpu_temperature
            last_update_time_temperature = current_time

        stdscr.refresh()
        time.sleep(0.005)  # Небольшая задержка для уменьшения нагрузки на CPU


def display_channels(stdscr, channels, start_line=1):
    # Отображаем данные каналов с учетом начальной строки
    for i, value in enumerate(channels, start=start_line):
        line = i + start_line - 1  # Вычисляем реальную строку для отображения
        stdscr.move(line, 0)
        stdscr.clrtoeol()
        stdscr.addstr(line, 0, f"Channel {i}: {value}")


if __name__ == "__main__":
    curses.wrapper(display_data_curses)


