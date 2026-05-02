from machine import Pin
import utime
from utime import sleep
import neopixel

class COMPONENTS():
    BUTTON = Pin(3, Pin.IN, Pin.PULL_DOWN)
    BUTTON_power = Pin(2, Pin.OUT)
    neopixel = neopixel.NeoPixel(Pin(1), 3)
    neopixel_power = Pin(0, Pin.OUT)
    BUZZER = Pin(14, Pin.OUT)

def Single_Press(components, count):
    print("SIGNLE PRESS")
    light = components.neopixel
    count += 1
    print(count)
    if count>5:
        components.BUZZER.value(1)
        sleep(1.5)
        components.BUZZER.value(0)
    else:
        for i in range (0, count):
            components.BUZZER.value(1)
            sleep(0.1)
            components.BUZZER.value(0)
            sleep(0.1)

    return count

def Double_Press(components, count):

    light = components.neopixel
    Pulse(light)
    count = 0
    print("double")

    return count   

def Pulse(light):
    Timer = utime.ticks_add(utime.ticks_ms(), 4000)
    while utime.ticks_diff(Timer, utime.ticks_ms()) > 0:
        for i in range(0, 50, 1):
            light[0] = (i*2, 0, 0)
            light.write()
            sleep(0.01)
        for j in range(50, 0, -1):
            light[0] = (j*2, 0, 0)
            light.write()
            sleep(0.01)
        
    light[0] = (0, 0, 0)
    light.write()

def Await_second_press():
    First_press_break = utime.ticks_add(utime.ticks_ms(), 1000)
    while utime.ticks_diff(First_press_break, utime.ticks_ms()) > 0:
                if COMPONENTS.BUTTON.value()==0:
                    sleep(0.05)
                    if COMPONENTS.BUTTON.value()==0:
                        while utime.ticks_diff(First_press_break, utime.ticks_ms()) > 0:
                            print("waiting")
                            #without this sleep a quick button click after a double click will cause another double click
                            if COMPONENTS.BUTTON.value()==1:
                                sleep(0.05)
                                if COMPONENTS.BUTTON.value()==1:
                                    return True
    return False

def main():
    count = 0
    Button_Reset = True
    COMPONENTS.BUTTON_power.value(1)
    COMPONENTS.neopixel_power.value(1)
    while True:
        if COMPONENTS.BUTTON.value()==1 and Button_Reset:
            print("click")
            Button_Reset = False
            Second_press = Await_second_press()
            if (Second_press):
                print("second click")
                count = Double_Press(COMPONENTS, count)
                if count>20:
                    count=20
            else:
                count = Single_Press(COMPONENTS, count)
                if count>20:
                    count=20
        if COMPONENTS.BUTTON.value()==0 and not Button_Reset:
            print("reset")
            Button_Reset = True
if __name__ == "__main__":
    main()
