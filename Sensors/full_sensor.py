import time
import csv
import board
import adafruit_bme680
import sys
import RPi.GPIO as GPIO

file_name = sys.argv[1]
run_time = int(sys.argv[2])

meta_data = ["Time","PM25","PM10","Temperature","Humidity","Pressure","CPS"]
file = open(file_name,"w",newline='')
data_writer = csv.writer(file)
data_writer.writerow(meta_data)

# Air Quality
reset_pin = None
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)

# Temperature, Pressure, and Humidity
i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
bme680.sea_level_pressure = 1013.25

# Radiation
tcounts = 0
ocounts = 0

def my_callback(channel):
    if GPIO.input(channel) == GPIO.FALLING:
        tcounts = tcounts + 1

delay = 0
time.sleep(delay)

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)
GPIO.add_event_detect(16, GPIO.FALLING, callback=my_callback)

now = time.time()
start_time = now

while  (now - start_time) < run_time:
    time.sleep(1)
    try:
        aqdata = pm25.read()
        print("Collecting data...")
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    scounts = tcounts - ocounts
    ocounts = tcounts

    now = time.time()

    data = [now,aqdata["pm25 standard"],aqdata["pm100 standard"],bme680.temperature,bme680.relative_humidity,bme680.pressure,scounts]    
    data_writer.writerow(data)

GPIO.cleanup()