from machine import Pin
import machine
import utime
from utime import sleep
import neopixel

class COMPONENTS():
    BUTTON = Pin(3, Pin.IN, Pin.PULL_DOWN)
    BUTTON_power = Pin(2, Pin.OUT)

    neopixel = neopixel.NeoPixel(Pin(1), 3) 
    neopixel_power = Pin(0, Pin.OUT)

    BUZZER = Pin(14, Pin.OUT)

    trigger = Pin(7, Pin.OUT, pull=0)
    echo = Pin(8, Pin.IN, pull=0)

    MOTOR_power = Pin(16, Pin.OUT)
    MOTOR_open = Pin(18, Pin.OUT)
    MOTOR_close = Pin(17, Pin.OUT)


def Single_Press(components, count):
    lights(components.neopixel, False)
    components.neopixel.write()
    count += 1
    Blink(components, count)
    
    components.MOTOR_power.value(1)
    sleep(0.2)
    motor(components, True)
    while components.BUTTON.value() == 0:
        pass
    motor(components, False)
    components.MOTOR_power.value(0)
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
        for i in range(0, 255, 5):
            light[0] = (i, 0, 0)
            light[1] = (i, 0, 0)
            light[2] = (i, 0, 0)
            light.write()
            sleep(0.01)
        for j in range(255, 0, -5):
            light[0] = (j, 0, 0)
            light[1] = (j, 0, 0)
            light[2] = (j, 0, 0)
            light.write()
            sleep(0.01)
        
    lights(light, False)

def Blink(components, count):
    for i in range (1, count+1):
        light_to_turn = (i % 3)
        if light_to_turn == 0:
            light_to_turn = 3
        components.neopixel[light_to_turn-1] = (255, 0, 0)
        components.neopixel.write()
        components.BUZZER.value(1)
        sleep(0.2)
        components.BUZZER.value(0)
        sleep(0.1)
        if i % 3 == 0:
            lights(components.neopixel, False)
            components.neopixel.write()

def Await_second_press():
    First_press_break = utime.ticks_add(utime.ticks_ms(), 1000)
    while utime.ticks_diff(First_press_break, utime.ticks_ms()) > 0:
                if COMPONENTS.BUTTON.value()==0:
                    sleep(0.05)
                    if COMPONENTS.BUTTON.value()==0:
                        while utime.ticks_diff(First_press_break, utime.ticks_ms()) > 0:
                            #without this sleep a quick button click after a double click will cause another double click
                            if COMPONENTS.BUTTON.value()==1:
                                sleep(0.05)
                                if COMPONENTS.BUTTON.value()==1:
                                    return True
    return False

def near(max_distance, components):
    trig = components.trigger 
    echo = components.echo
    trig.value(0)
    utime.sleep_us(2)

    trig.value(1)
    utime.sleep_us(10)
    trig.value(0)
    try:
            pulse_time = machine.time_pulse_us(echo, 1, 500*2*30)
            duration = pulse_time
            distance_cm = duration*0.0343/2
            sleep(0.1)
            if (distance_cm <= max_distance and distance_cm > 0):
                return True
    except OSError as ex:
        if ex.args[0] == 110: # 110 = ETIMEDOUT
            raise OSError('Out of range')
        raise ex


def motor(components, ON):
    if ON:
        First_press_break = utime.ticks_add(utime.ticks_ms(), 1150)
        components.MOTOR_open.value(1)
        while utime.ticks_diff(First_press_break, utime.ticks_ms()) > 0:
            print("open")
            print(components.MOTOR_open.value())
            print("closed")
            print(components.MOTOR_close.value())
            sleep(0.1)
            pass
    else:
        First_press_break = utime.ticks_add(utime.ticks_ms(), 1150)
        components.MOTOR_close.value(1)
        while utime.ticks_diff(First_press_break, utime.ticks_ms()) > 0:
            pass
    components.MOTOR_open.value(0)
    components.MOTOR_close.value(0)

def lights(light, ON):
    if ON:
        light[0] = (255, 0, 0)
        light[1] = (255, 0, 0)
        light[2] = (255, 0, 0)
    else:
        light[0] = (0, 0, 0)
        light[1] = (0, 0, 0)
        light[2] = (0, 0, 0)
    light.write()
    return

def main():
    MAX_DISTANCE = 20
    count = 0
    Button_Reset = True
    light = COMPONENTS.neopixel
    COMPONENTS.BUTTON_power.value(1)
    COMPONENTS.neopixel_power.value(1)
    while True:
        if (near(MAX_DISTANCE, COMPONENTS)):
            lights(light, True)
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
        else:
            lights(light, True)
if __name__ == "__main__":
    main()
