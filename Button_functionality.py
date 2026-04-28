from machine import Pin
from utime import sleep,ticks_ms , ticks_diff

class COMPONENTS():
    BUTTON = Pin(14, Pin.IN, Pin.PULL_DOWN)
    BUZZER = Pin(15, Pin.OUT)
    MOTOR = Pin(16, Pin.OUT)
    LED = Pin(17, Pin.OUT)

def Single_Press(components, count):
    count += 1
    for i in range(0, count):
        components.BUZZER.value(1)
        sleep(0.1)
        components.BUZZER.value(0)
        sleep(0.1)
    #TODO 
    #1.figure out how long to keep the motor on  
    #2.add in the second motor that locks/unlocks the drawer
    return count

def Double_Press(components, count):
    count = 0
    components.LED.value(0)
    sleep(0.3)
    components.LED.value(1)
    return count

def waitforrelease():
    # So that if the user is pressing the button for more than 1 second this will make sure that pico counts it as a single press
    while COMPONENTS.BUTTON.value() == 1:
        sleep(0.01)
    
def main():
    count = 0
    Second_Press = False
    Button_Reset = True
    while True:
        if COMPONENTS.BUTTON.value() == 1 and Button_Reset:
            Button_Reset = False
            if Second_Press:
                count = Double_Press(COMPONENTS, count)
            Second_Press = True
            sleep(3)
            count = Single_Press(COMPONENTS, count)
        if COMPONENTS.BUTTON.value()==0 and not Button_Reset:
            Button_Reset = True
