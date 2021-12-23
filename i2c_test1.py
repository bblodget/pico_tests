from machine import Pin, SoftI2C
from utime import sleep

sda=Pin(0, -1, Pin.PULL_UP)
scl=Pin(1, -1, Pin.PULL_UP)

i2c=SoftI2C(sda=sda, scl=scl, freq=100000)

print(i2c.scan())

def i2c_write(rb):
    i2c.start()
    b = bytearray(rb)
    print("b: ", b)
    n= i2c.write(b)
    i2c.stop()
    print("n: ", n)  


#reset
print("reset")
i2c_write([0x1C, 0xB0])

#Energize
print("energize")
i2c_write([0x1C, 0x85])

#set target velocity
print("target velocity")
i2c_write([0x1C, 0xE3, 0x80, 0x84, 0x1e, 0x00])



#i2c.writeto(14, '\xB0')

#Clear driver error
#i2c.writeto(14, '\x8A')

#Energize
#i2c.writeto(14, '\x85')

# Halt and set position
#i2c.writeto(14, '\xEC')

# Set target velocity
#vel = [0x80, 0x84, 0x1e, 0x00]
#b = bytearray(4)



#i2c.writeto_mem(14, 0xE3, b)

while True:
    sleep(1)
    
    






