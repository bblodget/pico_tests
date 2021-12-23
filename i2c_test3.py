from machine import Pin, I2C
from utime import sleep, sleep_ms

I2C_ADDR = 14

CMD_RESET = 0xB0
CMD_EXIT_SAFE_START = 0x83
CMD_ENTER_SAFE_START = 0x8F
CMD_ENERGIZE = 0x85
CMD_DEENERGIZE = 0x86
CMD_GET_VARIABLE = 0xA1

SET_TARGET_POSITION = 0xE0
SET_TARGET_VELOCITY = 0xE3

VAR_PLANNING_MODE = 0x09
VAR_CURRENT_POS = 0x22

sda=Pin(0, -1, Pin.PULL_UP)
scl=Pin(1, -1, Pin.PULL_UP)

i2c=I2C(0, sda=sda, scl=scl, freq=400000)

print(i2c.scan())

def startup():
    global i2c
    #reset
    print("reset")
    n=i2c.writeto(I2C_ADDR, bytearray([CMD_RESET]))
    print("n: ",n)
        
    #set target velocity to zero
    print("stop")
    n=i2c.writeto(I2C_ADDR, bytearray([SET_TARGET_VELOCITY, 0x00, 0x00, 0x00, 0x00]))
    print("n: ",n)

    #exit safe start
    print("exit safe start")
    n=i2c.writeto(I2C_ADDR, bytearray([CMD_EXIT_SAFE_START]))
    print("n: ",n)

    #Energize
    print("energize")
    n=i2c.writeto(I2C_ADDR, bytearray([CMD_ENERGIZE]))
    print("n: ",n)


def shutdown():
    global i2c
    print("de-energize")
    n=i2c.writeto(I2C_ADDR, bytearray([CMD_DEENERGIZE]))
    print("n: ",n)
    
    #enter safe start
    print("enter safe start")
    n=i2c.writeto(I2C_ADDR, bytearray([CMD_ENTER_SAFE_START])) 
    print("n: ",n)
    

def set_position(pos):
    global i2c
    print("set_position: ", pos)
    bpos = pos.to_bytes(4, 'little')
    n=i2c.writeto_mem(I2C_ADDR, SET_TARGET_POSITION, bpos)
    
    cur = None
    while cur != pos:
        bytes = get_variable(VAR_CURRENT_POS, 4)
        cur = int.from_bytes(bytes, 'little')
        print("cur: ",cur)
        sleep_ms(1000)
        
    print("cur==target: ",cur)
    
def set_velocity(vel):
    global i2c
    bvel = vel.to_bytes(4, 'little')
    n=i2c.writeto(14, SET_TARGET_VELOCITY, bvel)
    
def get_variable(offset, size):
    global i2c
    n=i2c.writeto(I2C_ADDR, bytearray([CMD_GET_VARIABLE, offset]))
    bytes=i2c.readfrom(I2C_ADDR, size)
    return bytes
    

startup()
target=200
set_position(target)
sleep_ms(100)
set_position(0)
sleep_ms(100)
shutdown()



#while True: 
#    sleep(1)
    
    






