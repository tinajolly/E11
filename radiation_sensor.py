import RPi.GPIO as GPIO
import datetime
import time
 
now = time.time()
start_time = time.time()
run_time = 20

#def my_callback(channel):
    #if GPIO.input(channel) == GPIO.FALLING:
        #print('Falling Edge at ' + str(datetime.datetime.now()))
 
while  ((now - start_time)) < run_time:

    GPIO.add_event_detect(channel, GPIO.FALLING)

    if GPIO.event_detected(channel):
        print('Falling Edge at ' + str(datetime.datetime.now()))

    #try:
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(6, GPIO.IN)
        #GPIO.add_event_detect(6, GPIO.BOTH, callback=my_callback)
        
 
    #finally:
        #GPIO.cleanup()