import board
import busio
import digitalio
import RPi.GPIO as GPIO
import  adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import time
import math

#Global Variables
t = 10
i = 0
time_befor = 0
Runtime = - int(time.time())

#Setup
def setup():
    print("Runtime     Temp Reading     Temp     Light Reading")
    global chan_0, chan_1, button
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)
    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
    # create an analog input channel on pin 0 and pin 1
    chan_0 = AnalogIn(mcp, MCP.P2)    #temp
    chan_1 = AnalogIn(mcp, MCP.P1)    #LDR
    #setup buttons 
    button = digitalio.DigitalInOut(board.D26)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

def btn_pressed():
    global t, i, button
    time.sleep(1)
    btn_thread = threading.Thread(target=btn_pressed)
    btn_thread.daemon = True
    btn_thread.start()
    if button.value == 0:
        # debouncing the button
        time.sleep(0.001)
        if button.value == 0:
            i += 1
            if i == 1:
                t=5.0
                pass
            elif i == 2:
                t=1.0
                pass
            elif i == 3:
                t = 10.0
                i = 0.0
                pass
        #print("button pressed  i = " + str(i) + "   t = " + str(t))
        print("button pressed")
        pass
    pass

def print_time_thread():
    global t, time_befor, Runtime, i


    thread = threading.Timer(t-0.01, print_time_thread)
    thread.daemon = True
    thread.start()
    time_now = time.time()
    Runtime += math.floor(time_now - time_befor)
    time_befor = time_now
    temp = int((chan_0.voltage-0.5)*100)
    
    if Runtime <= 9:
        print(str(Runtime) + "s           " + str(chan_0.value) + "          " + str(temp) + "C      " + str(chan_1.value))
    elif Runtime <=99:
        print(str(Runtime) + "s          " + str(chan_0.value) + "          " + str(temp) + "C      " + str(chan_1.value))
    elif Runtime <=999:
        print(str(Runtime) + "s         " + str(chan_0.value) + "          " + str(temp) + "C      " + str(chan_1.value))
        

if __name__ == "__main__":
    try:
        setup()
        print_time_thread()
        btn_pressed()
        while True:
            pass
    except Exception as e:
        print (e) 
    finally:
        GPIO.cleanup()
