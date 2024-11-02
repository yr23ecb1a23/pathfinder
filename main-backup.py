from src import test, robot_state, motor
import os
import sys
import threading
from time import sleep
import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt

# Setup module path
module_path = os.path.abspath("./build")
test.someRandomTest()
if module_path not in sys.path:
    sys.path.append(module_path)

# Motor class is imported from src.motor

# GPIO pins for ultrasonic sensor
TRIG = 4
ECHO = 5

# Setup GPIO for ultrasonic sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Constants for occupancy grid
GRID_SIZE = 20  # Size of the grid
GRID_SCALE = 10  # Scale for mapping distances to grid

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin):
        self.TRIG = trig_pin
        self.ECHO = echo_pin

    def get_distance(self):
        GPIO.output(self.TRIG, False)
        sleep(0.1)

        GPIO.output(self.TRIG, True)
        sleep(0.00001)
        GPIO.output(self.TRIG, False)

        start_time = time.time()
        while GPIO.input(self.ECHO) == 0:
            start_time = time.time()

        stop_time = time.time()
        while GPIO.input(self.ECHO) == 1:
            stop_time = time.time()

        time_elapsed = stop_time - start_time
        distance = (time_elapsed * 34300) / 2  # Distance in cm
        return distance

class SLAM:
    def __init__(self):
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE))
        self.x = GRID_SIZE // 2
        self.y = GRID_SIZE // 2
        self.angle = 0  # Angle in degrees

        # Initialize the motors (adjust pins as needed)
        self.right_motor = motor.Motor(24, 23, 25, 100, 0)  # Right motor GPIO pins
        self.left_motor = motor.Motor(17, 27, 22, 100, 0)   # Left motor GPIO pins

        # Initialize the ultrasonic sensor
        self.sensor = UltrasonicSensor(TRIG, ECHO)

    def move_forward(self):
        self.right_motor.move_forward()
        self.left_motor.move_forward()
        sleep(0.5)  # Move forward for a short duration
        self.right_motor.stop_motor()
        self.left_motor.stop_motor()

    def update_map(self):
        distance = self.sensor.get_distance()
        grid_x = int(self.x + distance * np.cos(np.radians(self.angle)) / GRID_SCALE)
        grid_y = int(self.y + distance * np.sin(np.radians(self.angle)) / GRID_SCALE)

        # Ensure we stay within grid boundaries
        if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
            self.grid[grid_y, grid_x] = 1  # Mark the grid cell as occupied

    def turn_left(self):
        self.angle = (self.angle + 15) % 360
        self.left_motor.move_reverse()  # Optional: modify behavior for turning
        self.right_motor.move_forward()  # Right motor goes forward
        sleep(0.5)  # Time to turn
        self.left_motor.stop_motor()
        self.right_motor.stop_motor()

    def turn_right(self):
        self.angle = (self.angle - 15) % 360
        self.left_motor.move_forward()  # Left motor goes forward
        self.right_motor.move_reverse()  # Right motor goes backward
        sleep(0.5)  # Time to turn
        self.left_motor.stop_motor()
        self.right_motor.stop_motor()

    def display_map(self):
        plt.figure(figsize=(10, 10))  # Set figure size
        plt.imshow(self.grid, cmap='Greys', origin='lower')
        plt.colorbar(label='Occupancy (1: Occupied, 0: Free)')
        plt.title('Occupancy Grid Map')
        plt.xlabel('Grid X Position')
        plt.ylabel('Grid Y Position')
        plt.savefig('occupancy_grid_map.png', bbox_inches='tight', dpi=300)  # Save with high resolution
        plt.show()  # Show the saved map

def main():
    # Initialize motors
    rightMotor = motor.Motor(24, 23, 25, 100, 0)  # Right motor
    leftMotor = motor.Motor(17, 27, 22, 100, 0)   # Left motor

    # Create SLAM instance
    slam = SLAM()

    try:
        while True:
            slam.move_forward()
            slam.update_map()
            # Randomly decide to turn left or right to explore the environment
            if np.random.random() < 0.5:
                slam.turn_left()
            else:
                slam.turn_right()
            sleep(0.5)  # Delay between movements

    except KeyboardInterrupt:
        print("Stopping SLAM...")
        slam.display_map()  # Display the map upon exiting
        rightMotor.stop_motor()
        leftMotor.stop_motor()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
