import machine
from machine import Pin, PWM
from dcmotor import DCMotor
from drive import Drive
from utime import sleep_ms
import sys
import uselect

min_duty_cycle = 15000
max_duty_cycle = 65535
frequency = 1000

right_pwm = PWM(Pin(2), frequency)
right_input_1 = Pin(3, Pin.OUT)
right_input_2 = Pin(4, Pin.OUT)

left_pwm = PWM(Pin(5), frequency)
left_input_1 = Pin(6, Pin.OUT)
left_input_2 = Pin(7, Pin.OUT)

rightWheel = DCMotor(right_input_1, right_input_2, right_pwm)
leftWheel = DCMotor(left_input_1, left_input_2, left_pwm)
drive = Drive(rightWheel, leftWheel)

poll = uselect.poll()
poll.register(sys.stdin, uselect.POLLIN)

def read_keyboard_input():
    # Check if an event has occurred on the registered streams with a 0ms timeout (non-blocking)
    if poll.poll(0):
        key = sys.stdin.read(1) # reads 1 character
        return key
    return None

print("Press 'q' to exit")
while True:
    char = read_keyboard_input()
    if char is not None:
        print(f"You pressed: {repr(char)}")
        if char == 'q':
            break
        if char == 'w':
            drive.forward(50)
        if char == 's':
            drive.reverse(50)
        if char == 'd':
            drive.right(50)
        if char == 'a':
            drive.left(50)
        if char == ' ':
            drive.stop()
        sleep_ms(100)
    else:
        drive.stop()

    sleep_ms(100)