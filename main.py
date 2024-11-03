from src import test, robot_state, motor
import os
import sys
import threading
from time import sleep
import time
import RPi.GPIO as GPIO
module_path = os.path.abspath("./build")
test.someRandomTest()
if module_path not in sys.path:
    sys.path.append(module_path)

is_on = True

TRIG = 4
ECHO = 5

# Set up the GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

is_path_blocked = False
def staller():
    global is_on
    is_on = True
    for i in range(0, 1000):
        while is_path_blocked:
            pass
        is_on = True
        sleep(0.01)
    is_on = False



def ultrasonic_thread():
    while True:
        global is_path_blocked

        # Set TRIG to HIGH for 10 microseconds
        GPIO.output(TRIG, True)
        sleep(0.00001)
        GPIO.output(TRIG, False)

        # Record the start time
        start_time = time.time()
        while GPIO.input(ECHO) == 0:
            start_time = time.time()

        # Record the arrival time
        stop_time = time.time()
        while GPIO.input(ECHO) == 1:
            stop_time = time.time()

        # Calculate the distance
        time_elapsed = stop_time - start_time
        distance = (time_elapsed * 34300) / 2  # Distance in cm

        if distance < 20:
            is_path_blocked = True
        else:
            is_path_blocked = False

        print(is_path_blocked)


rightMotor = motor.Motor(24, 23, 25, 100, 0)  # left motor
leftMotor = motor.Motor(17, 27, 22, 100, 0)
state = robot_state.RobotState()
rightMotor.move_forward()
rightMotor.set_motor_speed(50)
leftMotor.move_forward()
leftMotor.set_motor_speed(50)

obstacle_detection_thread = threading.Thread(target=ultrasonic_thread)
obstacle_detection_thread.start()

iterations = 0

inp = True
while inp:
    number_thread = threading.Thread(target=staller)
    leftMotor.move_forward()
    rightMotor.move_forward()
    number_thread.start()

    while is_on:
        angle = state.getAngleDegrees()

        if angle > 0.17:
            leftMotor.set_motor_speed(100-20)
            rightMotor.set_motor_speed(50-20)
        elif angle < -0.17:
            leftMotor.set_motor_speed(50-20)
            rightMotor.set_motor_speed(100-20)
        else:
            rightMotor.set_motor_speed(50)
            leftMotor.set_motor_speed(50)

        if is_path_blocked:
            rightMotor.stop_motor()
            leftMotor.stop_motor()
            sleep(0.2)
        else:
            rightMotor.move_forward()
            leftMotor.move_forward()
    number_thread.join()
    rightMotor.stop_motor()
    leftMotor.stop_motor()
    iterations += 1
    sleep(1)
    if iterations > 0:
        print("exiting")
        inp = False
    else:
        inp = True
        is_on = True
obstacle_detection_thread.join()
state.destroy()
