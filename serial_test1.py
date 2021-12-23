# Note:  Serial commands: https://www.pololu.com/docs/0J71/9


from machine import UART, Pin
from time import sleep, sleep_ms

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



def startup():
    global uart0
    
    #reset
    print("reset")
    send_command_header(CMD_RESET)
    #n=uart0.write(bytearray([CMD_RESET]))
    #print("n: ",n)
    
    #set target velocity to zero
    print("stop")
    set_velocity(0)
    
    #exit safe start
    print("exit safe start")
    send_command_header(CMD_EXIT_SAFE_START)
    #n=uart0.write(bytearray([CMD_EXIT_SAFE_START]))
    #print("n: ",n)
    
    #Energize
    print("energize")
    send_command_header(CMD_ENERGIZE)
    #n=uart0.write(bytearray([CMD_ENERGIZE]))
    #print("n: ",n)
    
def shutdown():
    print("de-energize")
    send_command_header(CMD_DEENERGIZE)
    
    print("enter safe start")
    send_command_header(CMD_ENTER_SAFE_START)

    
def set_velocity(vel):
    print("set_velocity: ", vel)
    command_w32(SET_TARGET_VELOCITY, vel)
    
    #bvel = vel.to_bytes(4, 'little')
    #n=uart0.write(bytearray([SET_TARGET_VELOCITY]) + bvel)
    #print("n: ",n)
    
def get_variable(offset, size):
    global uart0
    print("get_variable")
    n=uart0.write(bytearray([CMD_GET_VARIABLE, offset, size]))
    bytes=uart0.read(size)
    return bytes

def send_command_header(cmd):
    global uart0
    uart0.write(bytearray([cmd]))
    
def serial_w7(val):
    # Note we only write 7 bit values
    # So make msb 0.
    global uart0
    # print("serial_w7: ",val & 0x7F)
    uart0.write(bytearray([val & 0x7F]))
    
    

def command_w32(cmd, val):
    # command header
    send_command_header(cmd)
    
    # byte with MSbs:
    # bit 0 = MSb of first (least significant) data byte
    # bit 1 = MSb of second data byte
    # bit 2 = MSb of third data byte
    # bit 3 = MSb of fourth (most significant) data byte
    serial_w7(((val >>  7) & 1) |
           ((val >> 14) & 2) |
           ((val >> 21) & 4) |
           ((val >> 28) & 8))
    
    serial_w7(val >> 0); # least significant byte with MSb cleared
    serial_w7(val >> 8);
    serial_w7(val >> 16);
    serial_w7(val >> 24); # most significant byte with MSb cleared
    

def set_position(pos):
    print("set_position: ", pos)
    command_w32(SET_TARGET_POSITION, pos)

    
    cur = None
    while cur != pos:
        bytes = get_variable(VAR_CURRENT_POS, 4)
        cur = int.from_bytes(bytes, 'little')
        print("cur: ",cur)
        sleep_ms(100)
        
    print("cur==target: ",cur)
    
    
# Main
uart0 = UART(0, baudrate=115385, tx=Pin(0), rx=Pin(1))

startup()
sleep(1)

for _ in range(4):
    set_position(200)
    set_position(0)

sleep(1)

shutdown()



#txData = b'hello world\n\r'
#uart1.write(txData)
#time.sleep(0.1)
#rxData = bytes()
#while uart0.any() > 0:
#rxData += uart0.read(1)
#print(rxData.decode('utf-8'))
