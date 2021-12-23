from machine import Pin
from time import sleep

DELAY = 0.5 # seconds

p1 = Pin(2, Pin.OUT)
p2 = Pin(3, Pin.OUT)
p3 = Pin(4, Pin.OUT)
p4 = Pin(5, Pin.OUT)

def phase0():
    global p1, p2, p3, p4
    p1.value(0)
    p2.value(0)
    p3.value(0)
    p4.value(0)

def phase1():
    global p1, p2, p3, p4
    p1.value(1)
    p2.value(1)
    p3.value(0)
    p4.value(0)
             
def phase2():
    global p1, p2, p3, p4
    p1.value(0)
    p2.value(1)
    p3.value(1)
    p4.value(0)
    
def phase3():
    global p1, p2, p3, p4
    p1.value(0)
    p2.value(0)
    p3.value(1)
    p4.value(1)
    
def phase4():
    global p1, p2, p3, p4
    p1.value(1)
    p2.value(0)
    p3.value(0)
    p4.value(1)
    
def cw(steps, delay):
    for _ in range(steps):
        phase1()
        sleep(delay)
        phase2()
        sleep(delay)
        phase3()
        sleep(delay)
        phase4()
        sleep(delay)
    
def ccw(steps, delay):
    for _ in range(steps):
    