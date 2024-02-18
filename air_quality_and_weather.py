# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import csv
import board
import adafruit_bme680
import sys
# import busio
# from digitalio import DigitalInOut, Direction, Pull
# from adafruit_pm25.i2c import PM25_I2C

file_name = sys.argv[1]
run_time = int(sys.argv[2])

reset_pin = None

# For use with Raspberry Pi/Linux:
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

# Connect to a PM2.5 sensor over UART
from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)

i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
bme680.sea_level_pressure = 1013.25

meta_data = ["Time","PM25","PM10","Temperature","Humidity","Pressure"]
file = open(file_name,"w",newline='')
data_writer = csv.writer(file)
data_writer.writerow(meta_data)

start_time = time.time()
now = start_time

while (now - start_time) < run_time:
    try:
        aqdata = pm25.read()
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue
    
    now = time.time()

    print()
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")

    print()
    print("Temperature, Pressure, and Humidity")
    print("---------------------------------------")
    print("Temperature: %0.1f C" % bme680.temperature)
    print("Gas: %d ohm" % bme680.gas)
    print("Humidity: %0.1f %%" % bme680.relative_humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude: %0.2f meters" % bme680.altitude)
    print("---------------------------------------")

    data = [now,aqdata["pm25 standard"],aqdata["pm100 standard"],bme680.temperature,bme680.relative_humidity,bme680.pressure]    
    data_writer.writerow(data)

    print(now - start_time,"Seconds Since Start")
    time.sleep(1)