# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)


class Motor:
    def __init__(self, inlet1, inlet2, enable, digital_frequency, speed_offset):
        self.inlet1 = inlet1
        self.inlet2 = inlet2
        self.enable = enable
        self.speed_offset = speed_offset
        self.digital_frequency = digital_frequency
        GPIO.setup(self.inlet1, GPIO.OUT)
        GPIO.setup(self.inlet2, GPIO.OUT)
        GPIO.setup(self.enable, GPIO.OUT)
        GPIO.output(self.inlet1, GPIO.LOW)
        GPIO.output(self.inlet2, GPIO.LOW)
        self.pwm = GPIO.PWM(self.enable, self.digital_frequency)
        self.pwm.start(25+speed_offset)

    def stop_motor(self):
        GPIO.output(self.inlet1, GPIO.LOW)
        GPIO.output(self.inlet2, GPIO.LOW)

    def move_forward(self):
        GPIO.output(self.inlet1, GPIO.HIGH)
        GPIO.output(self.inlet2, GPIO.LOW)

    def move_reverse(self):
        GPIO.output(self.inlet1, GPIO.LOW)
        GPIO.output(self.inlet2, GPIO.HIGH)

    def set_motor_speed(self, speed):
        self.pwm.ChangeDutyCycle(speed+self.speed_offset)
        return True
try:
    motor1 = Motor(23, 24, 25, 100, 7)
    motor2 = Motor(27, 17, 22, 100, 0)

    motor1.move_forward()
    motor2.move_forward()
    sleep(10)

    motor1.move_reverse()
    motor2.move_reverse()

    sleep(10)

    motor1.stop_motor()
    motor2.stop_motor()

    GPIO.cleanup()
except KeyboardInterrupt:
    GPIO.cleanup()