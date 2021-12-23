from machine import Pin, Timer

def onTimeout(timer):
    global led
    led.toggle()

led = Pin(25, Pin.OUT)
tim = Timer()
tim.init(freq=5, mode=Timer.PERIODIC, callback=onTimeout)