from src import test, robot_state, motor
import os
import sys
import threading
from time import sleep
import cv2
import numpy as np

module_path = os.path.abspath("./build")
test.someRandomTest()
if module_path not in sys.path:
    sys.path.append(module_path)

is_on = True

# Initialize camera
cap = cv2.VideoCapture(0)  # Change 0 to the appropriate camera index if necessary

# Feature detector
orb = cv2.ORB_create()

# Define variables for visual odometry
prev_kp, prev_des = None, None
current_position = np.array([0.0, 0.0])  # Initialize position

def staller():
    global is_on
    is_on = True
    print("inside")
    sleep(1.6)
    is_on = False

rightMotor = motor.Motor(24, 23, 25, 100, 0)  # left motor
leftMotor = motor.Motor(17, 27, 22, 100, 0)
state = robot_state.RobotState()
rightMotor.move_forward()
rightMotor.set_motor_speed(50)
leftMotor.move_forward()
leftMotor.set_motor_speed(50)

inp = True
while inp:
    number_thread = threading.Thread(target=staller)
    leftMotor.move_forward()
    rightMotor.move_forward()
    number_thread.start()

    while is_on:
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect features
        kp, des = orb.detectAndCompute(gray, None)

        if prev_kp is not None and prev_des is not None:
            # Match features using BFMatcher
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(prev_des, des)
            matches = sorted(matches, key=lambda x: x.distance)

            # Extract matched keypoints
            prev_pts = np.float32([prev_kp[m.queryIdx].pt for m in matches]).reshape(-1, 2)
            curr_pts = np.float32([kp[m.trainIdx].pt for m in matches]).reshape(-1, 2)

            # Calculate the essential matrix and recover relative camera motion
            E, mask = cv2.findEssentialMat(curr_pts, prev_pts, focal=1, pp=(0, 0))
            points, R, t, mask = cv2.recoverPose(E, curr_pts, prev_pts)

            # Update position based on translation
            current_position += t.flatten()  # Simple update, consider scaling for real-world distance

            print("Current Position:", current_position)

        # Store current keypoints and descriptors
        prev_kp, prev_des = kp, des

        # Get angle and print information
        angle = state.getAngleDegrees()
        print(angle, state.getDisp())
        if angle > 0.17:
            leftMotor.set_motor_speed(100-40)
            rightMotor.set_motor_speed(50-40)
        elif angle < -0.17:
            leftMotor.set_motor_speed(50-40)
            rightMotor.set_motor_speed(100-40)
        else:
            rightMotor.set_motor_speed(50)
            leftMotor.set_motor_speed(50)

    number_thread.join()
    rightMotor.stop_motor()
    leftMotor.stop_motor()
    a = int(input())
    if a == 1:
        pass
    else:
        print("exiting")
        inp = False

cap.release()  # Release camera
state.destroy()
# pomafdspogpofas