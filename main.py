from machine import Pin
import machine
import utime
from utime import sleep
import neopixel

class COMPONENTS():
    """Class containing each component connected to the microcontroller"""
    #button
    BUTTON = Pin(3, Pin.IN, Pin.PULL_DOWN)
    BUTTON_power = Pin(2, Pin.OUT)

    #neopixel
    neopixel = neopixel.NeoPixel(Pin(1), 3) 
    neopixel_power = Pin(0, Pin.OUT)

    #buzzer
    BUZZER = Pin(14, Pin.OUT)

    #distance sensor
    trigger = Pin(7, Pin.OUT, pull=0)
    echo = Pin(8, Pin.IN, pull=0)

    #motor
    MOTOR_power = Pin(16, Pin.OUT)
    MOTOR_open = Pin(18, Pin.OUT)
    MOTOR_close = Pin(17, Pin.OUT)


def Single_Press(components, count):
    """Blinks the lights and buzzes the buzzer for each previous press, then opens the drawer and closes it again after second press, returns new count"""
    lights(components.neopixel, False)
    components.neopixel.write()
    count = min(count+1, 6) #clamps count to between 1 and 6
    Blink(components, count)

    #Unlike other components the motor only gets power when its about to be used
    components.MOTOR_power.value(1)
    motor(components, True)
    while components.BUTTON.value() == 0:
        pass #wait for second press
    motor(components, False)
    components.MOTOR_power.value(0)
    return count

def Double_Press(components, count):
    """Resets the count and pulses the neopixel, returns new count (0)"""
    light = components.neopixel
    Pulse(light)
    count = 0

    return count   

def Pulse(light):
    """Pulse the light for 4 seconds"""
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
    """Blinks the neopixels and buzzes the buzzer for each count one by one"""
    for i in range (1, count+1):
        #Check which light to turn on
        light_to_turn = (i % 3)
        if light_to_turn == 0:
            light_to_turn = 3
        components.neopixel[light_to_turn-1] = (255, 0, 0)
        components.neopixel.write()
        components.BUZZER.value(1)
        sleep(0.2)
        components.BUZZER.value(0)
        sleep(0.1)
        #Close lights when all three lights are open and not in the final run of the loop
        if i % 3 == 0 and not i == count:
            lights(components.neopixel, False)
            components.neopixel.write()

def Await_second_press():
    """Waits 1 second for another press, returns True if button is released and pressed during this period"""
    #This method used multiple times during the code, the while loop runs till the current ticks_ms() is equal to the calculated ending ticks_ms() at the start (1 second in this case)
    First_press_break = utime.ticks_add(utime.ticks_ms(), 1000) 
    while utime.ticks_diff(First_press_break, utime.ticks_ms()) > 0:
                    sleep(0.05)
                    if COMPONENTS.BUTTON.value()==0:
                        while utime.ticks_diff(First_press_break, utime.ticks_ms()) > 0:
                            #without this sleep a quick button click after a double click will cause another double click
                            if COMPONENTS.BUTTON.value()==1:
                                #Both sleeps are to ensure that the button is actually released and pressed and didint just vibrate up and down due to a soft press
                                sleep(0.05)
                                if COMPONENTS.BUTTON.value()==1:
                                    return True
    return False

def near(max_distance, components):
    """Checks if something is closer than max_distance (cm) and returns either True or False"""
    trig = components.trigger 
    echo = components.echo

    #Send 10 microsecond pulse
    trig.value(0)
    utime.sleep_us(2)
    trig.value(1)
    utime.sleep_us(10)
    trig.value(0)

    #calc the time time it takes to return the pulse
    pulse_time = machine.time_pulse_us(echo, 1, 500*2*30)
    duration = pulse_time
    #speed of sound = 343 m/s -> 0.0343 cm per microsecond (divided by 2 because sound needs to traver twice)
    distance_cm = duration*0.0343/2
    sleep(0.1)
    if (distance_cm <= max_distance and distance_cm > 0):
        return True


def motor(components, ON):
    """Turns the motor counterclockwise (TRUE) or counterclockwise (FALSE) for 1.150 seconds"""
    if ON:
        components.MOTOR_open.value(1)
        sleep(1.150)
    else:
        components.MOTOR_close.value(1)
        sleep(1.150)
    #Makes sure neither logic pin stays on
    components.MOTOR_open.value(0)
    components.MOTOR_close.value(0)

def lights(light, ON):
    """Turns all the lights in the 3 pixel neopixel either on (TRUE) or off (FALSE)"""
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
    #Power the button and neopixel
    COMPONENTS.BUTTON_power.value(1)
    COMPONENTS.neopixel_power.value(1)
    while True:
        if (near(MAX_DISTANCE, COMPONENTS)):
            #If someone is near, turn lights on and start checking for button presses
            lights(light, True)
            if COMPONENTS.BUTTON.value() == 1 and Button_Reset:
                Button_Reset = False
                Second_press = Await_second_press()
                if Second_press:
                    count = Double_Press(COMPONENTS, count)
                else:
                    count = Single_Press(COMPONENTS, count)
            if COMPONENTS.BUTTON.value() == 0 and not Button_Reset:
                #Force the button to be released before its counted again
                Button_Reset = True
        else:
            #If noone is near, turn lights off
            lights(light, False)

if __name__ == "__main__":
    main()
