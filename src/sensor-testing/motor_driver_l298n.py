# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/
import threading
import RPi.GPIO as GPIO
from time import sleep
import time

import board
import busio
import adafruit_mpu6050
import math

# Create I2C object using the appropriate pins
i2c = busio.I2C(board.SCL, board.SDA)

# Create the MPU6050 object
mpu = adafruit_mpu6050.MPU6050(i2c)

GPIO.setmode(GPIO.BCM)


def calculateError():
    c = 0
    AccErrorX = 0
    AccErrorY = 0
    while c < 200:
        AccX, AccZ, AccY = mpu.acceleration
        AccErrorX += (math.atan(AccY / math.sqrt(AccX ** 2 + AccZ ** 2)) * 180 / math.pi)
        AccErrorY += (math.atan(-1 * (AccX) / math.sqrt(pow((AccY), 2) + pow((AccZ), 2))) * 180 / math.pi)
        c += 1
    AccErrorX = AccErrorX / 200
    AccErrorY = AccErrorY / 200
    c = 0

    GyroErrorX = 0
    GyroErrorY = 0
    GyroErrorZ = 0
    while c < 200:
        GyroX, GyroY, GyroZ = mpu.gyro
        GyroErrorX += GyroX
        GyroErrorY += GyroY
        GyroErrorZ += GyroZ
        c += 1
    GyroErrorX = GyroErrorX / 200
    GyroErrorY = GyroErrorY / 200
    GyroErrorZ = GyroErrorZ / 200
    return AccErrorX, AccErrorY, GyroErrorX, GyroErrorY, GyroErrorZ


stop_thread = False

# def non_blocking_task():
#     # Use append mode to keep the previous data
#     with open("acceleration_values.txt", "a") as file:
#         while not stop_thread:
#             print("Running non-blocking task in a separate thread...")
#             # Add a small delay to prevent CPU overload
#             time.sleep(0.2)
#
#             # Retrieve the acceleration values (assuming they are floats)
#             x, y, z = mpu.acceleration
#
#             # Convert float values to strings and write to the file
#             file.write(f"{x}-x {y}-y {z}-z\n")  # Using f-strings for formatting
#
#
# # Start the non-blocking task in a new thread
# task_thread = threading.Thread(target=non_blocking_task)
# task_thread.start()

try:
    motor1 = Motor(24, 23, 25, 100, 0)  # left motor
    motor2 = Motor(17, 27, 22, 100, 0)

    motor1.set_motor_speed(50)
    motor2.set_motor_speed(50)
    # motor1.move_forward()
    # motor2.move_forward()
    # sleep(0.2)

    #motor1.move_reverse()
    #motor2.move_reverse()

    #sleep(0.8)
   # stop_thread = True
    AccErrorX, AccErrorY, GyroErrorX, GyroErrorY, GyroErrorZ = calculateError()
    accAngleZ, accAngleX, gyroAngleX, gyroAngleY, gyroAngleZ = 0, 0, 0, 0, 0
    yaw = 0
    previous_time = time.time()
    angle = 0
    velocity = 0
    distance = 0
    while True:
        motor1.move_forward()
        motor1.set_motor_speed(50)
        motor2.move_forward()
        motor2.set_motor_speed(50)
        if(angle*180/math.pi < -3):
            motor1.set_motor_speed(100)
        if(angle*180/math.pi > 3):
            motor2.set_motor_speed(100)
        current_time = time.time()
        elapsedTime = current_time - previous_time
        AccX, AccZ, AccY = mpu.acceleration
        GyroX, GyroY, GyroZ = mpu.gyro
        GyroX -= GyroErrorX
        GyroY -= GyroErrorY
        GyroZ -= GyroErrorZ
        accAngleX = (math.atan(AccY / math.sqrt(AccX**2 + AccZ**2)) * 180 / math.pi) - AccErrorX
        accAngleY = (math.atan(-AccX / math.sqrt(AccY**2 + AccZ**2)) * 180 / math.pi) - AccErrorY
        # // Currently the raw values are in degrees per seconds, deg/s, so we need to multiply by sendonds (s) to get the angle in degrees
        gyroAngleZ += GyroZ * elapsedTime
        gyroAngleX += GyroX * elapsedTime
        yaw += GyroY * elapsedTime
        roll = 0.96 * gyroAngleZ + 0.04 * accAngleZ
        pitch = 0.96 * gyroAngleX + 0.04 * accAngleX
        angle = roll
        acc = AccX - AccErrorX
        velocity += (acc * elapsedTime)
        distance += velocity*elapsedTime + (0.5*acc*(elapsedTime**2))
        print(angle*180/math.pi, (pitch*180)/math.pi, "displacement is ", distance)
        if(angle*180/math.pi < -3):
            motor1.set_motor_speed(100)
        if(angle*180/math.pi > 3):
            motor2.set_motor_speed(100)
        previous_time = current_time

    GPIO.cleanup()
except KeyboardInterrupt:
    motor1.stop_motor()
    motor2.stop_motor()
    GPIO.cleanup()
