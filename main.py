from machine import Pin
import utime
from utime import sleep
import neopixel
import math 

class COMPONENTS():
    BUTTON = Pin(14, Pin.IN, Pin.PULL_DOWN)
    neopixel = neopixel.NeoPixel(Pin(2), 8)

def Single_Press(components, count):
    print("SIGNLE PRESS")
    light = components.neopixel
    count =+ 1
    for i in range (0, count):
        light[i] = (255, 0, 0)
        light[i].write()
        light[i] = (0, 0, 0)
        light[i].write()

    return count

def Double_Press(components, count):
    light = components.neopixel
    Pulse(light, 50)
    count = 0
    return count

def Pulse(neopixel, t):
    for i in range(20):
        neopixel.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
        sleep(t/1000)

def main():
    Button_Reset = True
    Second_Press = False
    while True:
        if COMPONENTS.BUTTON.value()==1 and Button_Reset:
            print("click")
            First_press_time_break = utime.time()+3
            Button_Reset = False
            while utime.time()<First_press_time_break and not Second_Press:
                if COMPONENTS.BUTTON.value()==0:
                    while utime.time()<First_press_time_break and not Second_Press:
                        #without this sleep a quick button click after a double click will cause another double click
                        sleep(0.1)
                        if COMPONENTS.BUTTON.value()==1:
                            Second_Press = True
                            break
            if Second_Press:
                Double_Press(COMPONENTS, 1)
            else:
                Single_Press(COMPONENTS, 1)
            sleep(1)
        if COMPONENTS.BUTTON.value()==0 and not Button_Reset:
            print("reset")
            Button_Reset = True
            Second_Press = False

main()
