import RPi.GPIO as GPIO
import datetime
import time
import sys
import csv

file_name1 = sys.argv[1]
file_name2 = sys.argv[2]
run_time = int(sys.argv[3])

meta_data = ["Minute","Counts per Minute"]
file = open(file_name1,"w",newline='')
data_writer = csv.writer(file)
data_writer.writerow(meta_data)

meta_data = ["Counts"]
file = open(file_name2,"w",newline='')
data_writer = csv.writer(file)
data_writer.writerow(meta_data)

tcounts = 0
ocounts = 0
t = 0

def my_callback(channel):
    if GPIO.input(channel) == GPIO.FALLING:
        #print('Count at ' + str(datetime.datetime.now()))
        tcounts = tcounts + 1
        data1 = [str(datetime.datetime.now())]
        data_writer.writerow(data1)

now = time.time()
start_time = now

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)
GPIO.add_event_detect(16, GPIO.FALLING, callback=my_callback)
 
while  ((now - start_time)) < run_time:
    time.sleep(60)
    now = time.time()
    t = t + 1
    mcounts = tcounts - ocounts
    ocounts = tcounts
    print("Counts per Mintue =", mcounts)
    data2 = [t,mcounts]
    data_writer.writerow(data2)

GPIO.cleanup()