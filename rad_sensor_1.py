import RPi.GPIO as GPIO
import datetime
import time
#import board

now = time.time()
start_time = time.time()
run_time = 20

def my_callback(channel):
    if GPIO.input(channel) == GPIO.LOW:
        print('Count at ' + str(datetime.datetime.now()))
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)
GPIO.add_event_detect(16, GPIO.FALLING, callback=my_callback)



while now - start_time < 20 :
    time.sleep(1)
    
