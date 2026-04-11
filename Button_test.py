from machine import Pin
import utime
from utime import sleep

class COMPONENTS():
    BUTTON = Pin(14, Pin.IN, Pin.PULL_DOWN)

def Single_Press(count):
    print("SIGNLE PRESS")
    return count

def Double_Press(count):
    print("DOUBLE PRESS")
    return count
    
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
                Double_Press(1)
            else:
                Single_Press(1)
            sleep(1)
        if COMPONENTS.BUTTON.value()==0 and not Button_Reset:
            print("reset")
            Button_Reset = True
            Second_Press = False

main()