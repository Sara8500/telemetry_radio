import serial
import time

# baudrate: 57600 Bits/second -> 7200 Bytes/s

serial_port = '/dev/ttyUSB1'
baud_rate = 57600
message = b"AITtodaytomorrowAITtodaytomorrow"
sleep_time = 0.01   # seconds
duration_transmission = 60  # seconds


print('message : ', message, '\nmessage length : ', len(message))

# open serial port
with serial.Serial(serial_port, baud_rate) as ser:
    print(ser.name)

    # send data:
    for t in range(round(duration_transmission/sleep_time)):
        ser.write(message)
        time.sleep(sleep_time)
