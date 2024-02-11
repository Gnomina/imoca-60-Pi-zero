import read_sbus_from_GPIO
import time

SBUS_PIN = 4  # pin where sbus wire is plugged in

reader = read_sbus_from_GPIO.SbusReader(SBUS_PIN)
reader.begin_listen()

print("Waiting for connection...")

# wait until connection is established
while not reader.is_connected():
    print(".", end="", flush=True)
    time.sleep(.2)

print("\nConnected. Waiting for data stabilization...")
# Note that there will be nonsense data for the first 10ms or so of connection
# until the first packet comes in.
time.sleep(.1)

print("Starting to read SBUS data:")

# Initialize the last_time variable with the current time
last_time = time.time()

while True:
    try:
        is_connected = reader.is_connected()
        packet_age = reader.get_latest_packet_age()  # milliseconds

        # returns list of length 16, so -1 from channel num to get index
        channel_data = reader.translate_latest_packet()

        # Calculate the time difference
        current_time = time.time()
        time_difference = current_time - last_time
        last_time = current_time

        # Print the channel data and time difference to see the output
        print(f'Channel Data: {channel_data}')
        print(f'Time between packets: {time_difference:.2f}sec')

        time.sleep(0.5)  # Add delay to make the output more readable

    except KeyboardInterrupt:
        # cleanup cleanly after ctrl-c
        print("\nExiting due to keyboard interrupt.")
        reader.end_listen()
        exit()
    except Exception as e:
        # cleanup cleanly after error
        print(f"Error: {e}")
        reader.end_listen()
        raise
