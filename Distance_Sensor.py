from machine import Pin
from utime import sleep, sleep_us, ticks_us, ticks_diff

trig = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)
led = Pin("LED", Pin.OUT)

football = 20   # distance limit in cmeteres8

def get_distance():
    trig.value(0)
    sleep_us(2)

    trig.value(1)
    sleep_us(10)
    trig.value(0)

    start_time = ticks_us()

    while echo.value() == 0:
        if ticks_diff(ticks_us(), start_time) > 30000:
            return -1

    pulse_start = ticks_us()

    start_time = ticks_us()

    while echo.value() == 1:
        if ticks_diff(ticks_us(), start_time) > 30000:
            return -1

    pulse_end = ticks_us()

    duration = ticks_diff(pulse_end, pulse_start)
    distance_cm = duration * 0.0343 / 2

    return distance_cm

while True:
    distance = get_distance()
    print(distance)

    if distance > 0 and distance < football: 
        led.value(1)
        print("someone is NEAR")
    else:
        led.value(0)
        print("area is clear")

    sleep(0.3)
  
