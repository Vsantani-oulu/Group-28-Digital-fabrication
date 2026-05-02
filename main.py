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

    TRIG_sensor = Pin(6, Pin.OUT)
    ECHO_sensor = Pin(7, Pin.IN)

    MOTOR = Pin(28, Pin.OUT)


def Single_Press(components, count):
    print("SIGNLE PRESS")
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

def near(max_distance, components):
    trig = components.TRIG_sensor 
    echo = components.ECHO_sensor

    trig.value(0)
    utime.sleep_us(2)

    trig.value(1)
    utime.sleep_us(10)
    trig.value(0)

    start_time = utime.ticks_us()

    while echo.value() == 0:
        if utime.ticks_diff(utime.ticks_us(), start_time) > 30000:
            return -1

    pulse_start = utime.ticks_us()

    start_time = utime.ticks_us()

    while echo.value() == 1:
        if utime.ticks_diff(utime.ticks_us(), start_time) > 30000:
            return -1

    pulse_end = utime.ticks_us()

    duration = utime.ticks_diff(pulse_end, pulse_start)
    distance_cm = duration * 0.0343 / 2

    return (distance_cm > max_distance and distance_cm < 0)

def main():
    MAX_DISTANCE = 20
    count = 0
    Button_Reset = True
    COMPONENTS.BUTTON_power.value(1)
    COMPONENTS.neopixel_power.value(1)
    while True:
        while near(MAX_DISTANCE, COMPONENTS):
            COMPONENTS.neopixel[0] = (50, 0, 0)
            COMPONENTS.neopixel.write()
            if COMPONENTS.BUTTON.value() == 1 and Button_Reset:
                print("click")
                Button_Reset = False
                Second_press = Await_second_press()
                if (Second_press):
                    print("second click")
                    count = Double_Press(COMPONENTS, count)
                    if count > 20:
                        count = 20
                else:
                    count = Single_Press(COMPONENTS, count)
                    if count > 20:
                        count = 20
            if COMPONENTS.BUTTON.value() == 0 and not Button_Reset:
                print("reset")
                Button_Reset = True
        COMPONENTS.neopixel[0] = (0, 0, 0)
        COMPONENTS.neopixel.write()
        sleep(0.5)

if __name__ == "__main__":
    main()
