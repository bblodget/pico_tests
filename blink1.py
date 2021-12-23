from machine import Pin
from utime import sleep

DELAY = 0.5 # seconds

led = Pin(25, Pin.OUT)

while True:
    led.value(1)
    sleep(DELAY)
    led.value(0)
    sleep(DELAY)
    
 
    
