import threading
import RPi.GPIO as GPIO
from time import sleep
import time

import board
import busio
import adafruit_mpu6050
import math

def calculateError(mpu):
    c = 0
    AccErrorX = 0
    AccErrorY = 0
    AbsAccErrorX = 0
    while c < 200:
        AccX, AccZ, AccY = mpu.acceleration
        AbsAccErrorX += AccX
        AccErrorX += (math.atan(AccY / math.sqrt(AccX ** 2 + AccZ ** 2)) * 180 / math.pi)
        AccErrorY += (math.atan(-1 * (AccX) / math.sqrt(pow((AccY), 2) + pow((AccZ), 2))) * 180 / math.pi)
        c += 1
    AbsAccErrorX = AbsAccErrorX / 200
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
    return AbsAccErrorX, AccErrorX, AccErrorY, GyroErrorX, GyroErrorY, GyroErrorZ


class RobotState:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mpu = adafruit_mpu6050.MPU6050(i2c)
        self.AbsAccErrorX, self.AccErrorX, self.AccErrorY, self.GyroErrorX, self.GyroErrorY, self.GyroErrorZ = calculateError(self.mpu)
        self._runningState = True
        self._angle = 0
        self._distance = 0
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._state_updater)
        self._thread.start()
        self._prev_speed = 0
        self._speed = 0
        self._absolute_disp = 0

    def _state_updater(self):
        accAngleZ, accAngleX, gyroAngleX, gyroAngleY, gyroAngleZ = 0, 0, 0, 0, 0
        yaw = 0
        previous_time = time.time()
        while self._runningState:
            current_time = time.time()
            elapsedTime = current_time - previous_time
            AccX, AccZ, AccY = self.mpu.acceleration
            GyroX, GyroY, GyroZ = self.mpu.gyro
            GyroX -= self.GyroErrorX
            GyroY -= self.GyroErrorY
            GyroZ -= self.GyroErrorZ
            AccX -= self.AbsAccErrorX
            self._speed = self._prev_speed + (AccX * elapsedTime)
            self._absolute_disp += (self._prev_speed*elapsedTime) + (AccX * (elapsedTime**2)/2)
            print(self._absolute_disp, "metres")
            accAngleX = (math.atan(AccY / math.sqrt(AccX ** 2 + AccZ ** 2)) * 180 / math.pi) - self.AccErrorX
            accAngleY = (math.atan(-AccX / math.sqrt(AccY ** 2 + AccZ ** 2)) * 180 / math.pi) - self.AccErrorY
            gyroAngleZ += GyroZ * elapsedTime
            gyroAngleX += GyroX * elapsedTime
            yaw += GyroY * elapsedTime
            roll = 0.96 * gyroAngleZ + 0.04 * accAngleZ
            pitch = 0.96 * gyroAngleX + 0.04 * accAngleX
            self._prev_speed = self._speed
            with self._lock:
                self._angle = roll
            previous_time = current_time

    def destroy(self):
        self._runningState = False
        self._thread.join()
        GPIO.cleanup()

    def getAngle(self):
        with self._lock:
            return self._angle

    def getAngleDegrees(self):
        with self._lock:
            return self._angle * 180 / math.pi