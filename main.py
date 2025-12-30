import asyncio

from dcmotor import DCMotor
from drive import Drive
from machine import Pin, PWM
import aioble
import bluetooth
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

# NUS UUIDs
_UART_UUID = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
_UART_TX_UUID = bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E')
_UART_RX_UUID = bluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E')

# Register GATT server
uart_service = aioble.Service(_UART_UUID)
tx_characteristic = aioble.Characteristic(
    uart_service, _UART_TX_UUID, read=True, notify=True
)
rx_characteristic = aioble.Characteristic(
    uart_service, _UART_RX_UUID, write=True, capture=True
)
aioble.register_services(uart_service)

def control_car(cmd):
    if cmd == 'ping':
        print("Ping request!")

    if cmd == 'forward':
        print("Forward request!")
        drive.forward(100)

    if cmd == 'reverse':
        print("Reverse request!")
        drive.reverse(100)

    if cmd == 'right':
        print("Right request!")
        drive.right(75)

    if cmd == 'left':
        print("Left request!")
        drive.left(75)

    if cmd == 'stop':
        print("Stop request!")
        drive.stop()

# Serially wait for connections. Don't advertise while a central is connected.
async def peripheral_task():
    while True:
        async with await aioble.advertise(
            100_000,  # advertising interval (us)
            name="RCCar",
            services=[_UART_UUID],
        ) as connection:
            print("Connection from", connection.device)

            async def handle_rx():
                while True:
                    _, value = await rx_characteristic.written()
                    cmd = value.decode('utf-8').strip()
                    print("Received command:", cmd)
                    control_car(cmd)

            rx_task = asyncio.create_task(handle_rx())
            await connection.disconnected()
            rx_task.cancel()
            print("Disconnected")

asyncio.run(peripheral_task())