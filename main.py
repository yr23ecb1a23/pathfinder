from src import test, robot_state, motor, backend
import os
import sys
import threading
import requests
from time import sleep
import time
import RPi.GPIO as GPIO

module_path = os.path.abspath("./build")
test.someRandomTest()
if module_path not in sys.path:
    sys.path.append(module_path)

is_on = True
is_thread_on = True
TRIG = 4
ECHO = 5

# Set up the GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

is_path_blocked = False


def staller():
    global is_on
    is_on = True
    for i in range(0, 160):
        while is_path_blocked:
            pass
        is_on = True
        sleep(0.01)
    is_on = False


us_lock = threading.Lock()

def backend_thread():
    backend.app.run(host='0.0.0.0', port=5000)
backend_thread_obj = threading.Thread(target=backend_thread)
backend_thread_obj.start()
def ultrasonic_thread():
    while is_thread_on:
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
            with us_lock:
                is_path_blocked = True
        else:
            with us_lock:
                is_path_blocked = False

        # print(is_path_blocked)

current_destination = -1
def poll_backend(url):
    global current_destination
    while True:
        try:
            response = requests.get(url)
            data = response.json()

            current_destination = data.get('current_destination', -1)
            print(f"Current destination: {current_destination}")

            if current_destination != -1:
                print("Destination has been set, exiting polling.")
                break
            print("Polling again")
            time.sleep(1)  # Wait before polling again
        except requests.exceptions.RequestException as e:
            print(f"Error while polling: {e}")
            time.sleep(2)  # Wait a bit longer on error
backend_url = 'http://localhost:5000/get_destination'  # Use localhost for local testing
delivery_url = 'http://localhost:5000/get_delivery_done'
poll_backend(backend_url)

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
u_turn_done = False
inp = True
delta = 0.17
delta2 = -0.17
while inp:
    number_thread = threading.Thread(target=staller)
    leftMotor.move_forward()
    rightMotor.move_forward()
    number_thread.start()
    if u_turn_done:
        delta = 180.5
        delta2 = 179.5
    while is_on:
        angle = state.getAngleDegrees()
        print(angle)
        if angle > delta:
            leftMotor.set_motor_speed(100 - 20)
            rightMotor.set_motor_speed(50 - 20)
        elif angle < delta2:
            leftMotor.set_motor_speed(50 - 20)
            rightMotor.set_motor_speed(100 - 20)
        else:
            rightMotor.set_motor_speed(50)
            leftMotor.set_motor_speed(50)
        with us_lock:
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
    if iterations > current_destination-1:
        while True:
            try:
                response = requests.get(delivery_url)
                data = response.json()

                is_delivery_done = data.get('delivery', False)
                print(f"delivery done {is_delivery_done}")

                if is_delivery_done == True:
                    print("Delivery is done")
                    break
                print("Polling again")
                time.sleep(1)  # Wait before polling again
            except requests.exceptions.RequestException as e:
                print(f"Error while polling: {e}")
                time.sleep(2)  # Wait a bit longer on error
        sleep(1)
        if u_turn_done:
            leftMotor.stop_motor()
            rightMotor.stop_motor()
            break
        leftMotor.set_motor_speed(100-50)
        rightMotor.set_motor_speed(70-50)
        leftMotor.move_reverse()
        rightMotor.move_forward()
        while not u_turn_done:
            angle = state.getAngleDegrees()
            print(angle)
            if angle < 176:
                leftMotor.move_reverse()
                rightMotor.move_forward()
            elif angle > 186:
                leftMotor.move_forward()
                rightMotor.move_reverse()
            else:
                break

        leftMotor.set_motor_speed(50)
        rightMotor.set_motor_speed(50)
        leftMotor.move_forward()
        rightMotor.move_forward()
        state.resetAngle()
        u_turn_done = True
        iterations = 0
        print("initiating back")
        inp = True
        is_on = True
    else:
        inp = True
        is_on = True

is_thread_on = False
obstacle_detection_thread.join()
state.destroy()
backend_thread_obj.join()