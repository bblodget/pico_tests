from machine import Pin, Timer
from utime import sleep, ticks_us, sleep_us, ticks_diff

THRESHOLD = 600

ctrl = Pin(28, Pin.OUT)

sig_pins = [ 
    Pin(26, Pin.OUT),
    Pin(22, Pin.OUT),
    Pin(21, Pin.OUT),
    Pin(20, Pin.OUT),
    Pin(19, Pin.OUT),
    Pin(18, Pin.OUT),
    Pin(17, Pin.OUT),
    Pin(16, Pin.OUT)
]


def read_line_sensor():
    global ctrl
    global sig_pins
    
    ret = [-1, -1, -1, -1, -1, -1, -1, -1]
    
    # Turn on the emitters
    ctrl.value(1)
    
    # Set all sig pins to outputs
    # and set to 1.
    for sig in sig_pins:
        sig.init(Pin.OUT)
        sig.value(1)
        
    # sleep 10us to enable charge
    sleep_us(10)
    
    # Change the sigs to inputs
    for sig in sig_pins:
        sig.init(Pin.IN)
        
    # start a timer
    t1 = ticks_us()
    
    # Count how long it takes for
    # sigs to go low
    sig_count = 0
    while sig_count<len(sig_pins):
        for i, sig in enumerate(sig_pins):
            if sig.value()==0 and ret[i]==-1:
                t2 = ticks_us()
                if ticks_diff(t2, t1) > THRESHOLD:
                    ret[i] = 1
                else:
                    ret[i] = 0
                sig_count = sig_count + 1
        
    # Turn off the emitters to save power
    ctrl.value(0)
        
    return ret
            
while True:
    values = read_line_sensor()        
    print("values: ", values)
    #sleep(.1)



