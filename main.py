from dcmotor import DCMotor
from drive import Drive
from machine import Pin, PWM
import network
import secrets
import socket
import sys
import uselect
from utime import sleep_ms

# Used the following Raspberry Pi Article to create the Web Server:
# https://www.raspberrypi.com/news/how-to-run-a-webserver-on-raspberry-pi-pico-w/
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Waiting for network connection...')
    sleep_ms(1000)

if wlan.status() != 3:
    print(str(wlan.status()) + ' network status.')
    raise RuntimeError('Network connection failed!')
else:
    print('Connected successfully to the network!')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)
print('Listening on', addr)

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

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)

        request = str(request)
        ping_request = request.find('/drive/ping')
        forward_request = request.find('/drive/forward')
        reverse_request = request.find('/drive/reverse')
        right_request = request.find('/drive/right')
        left_request = request.find('/drive/left')
        stop_request = request.find('/drive/stop')

        print('ping_request = ' + str(ping_request))
        print('forward_request = ' + str(forward_request))
        print('reverse_request = ' + str(reverse_request))
        print('right_request = ' + str(right_request))
        print('left_request = ' + str(left_request))
        print('stop_request = ' + str(stop_request))

        lastState = None

        if ping_request == 6:
            print("Ping request!")
            lastState = "ping"

        if forward_request == 6:
            print("Forward request!")
            drive.forward(50)
            lastState = "forward"

        if reverse_request == 6:
            print("Reverse request!")
            drive.reverse(50)
            lastState = "reverse"

        if right_request == 6:
            print("Right request!")
            drive.right(50)
            lastState = "right"

        if left_request == 6:
            print("Left request!")
            drive.left(50)
            lastState = "left"

        if stop_request == 6:
            print("Stop request!")
            drive.stop()
            lastState = "stop"

        responseBody = '{ "lastState": "' + lastState + '"}'
        print('Response Body: ' + responseBody)

        cl.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
        cl.send(responseBody)
        cl.close()

    except OSError as e:
        cl.close()
        print('Network connection closed!')

    sleep_ms(100)