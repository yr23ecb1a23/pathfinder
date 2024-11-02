import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import time

# Constants for the grid and movement
GRID_SIZE = 20  # Size of the grid
GRID_SCALE = 10  # Scale for mapping distances to grid
ANGLE_CHANGE = 15  # Degrees to turn left or right

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin):
        self.TRIG = trig_pin
        self.ECHO = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

    def get_distance(self):
        GPIO.output(self.TRIG, False)
        sleep(0.1)  # Short delay

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

    def cleanup(self):
        GPIO.cleanup()

class Motor:
    def __init__(self, pin_a, pin_b, pwm_pin):
        self.pin_a = pin_a
        self.pin_b = pin_b
        GPIO.setup(self.pin_a, GPIO.OUT)
        GPIO.setup(self.pin_b, GPIO.OUT)
        self.pwm = GPIO.PWM(pwm_pin, 100)  # Frequency of 100Hz
        self.pwm.start(0)

    def move_forward(self):
        GPIO.output(self.pin_a, GPIO.HIGH)
        GPIO.output(self.pin_b, GPIO.LOW)

    def stop_motor(self):
        GPIO.output(self.pin_a, GPIO.LOW)
        GPIO.output(self.pin_b, GPIO.LOW)

    def set_speed(self, speed):
        self.pwm.ChangeDutyCycle(speed)

class SLAM:
    def __init__(self):
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE))
        self.x = GRID_SIZE // 2
        self.y = GRID_SIZE // 2
        self.angle = 0  # Angle in degrees

        # Initialize the motors
        self.right_motor = Motor(24, 23, 25)  # Right motor GPIO pins
        self.left_motor = Motor(17, 27, 22)   # Left motor GPIO pins

        # Initialize the ultrasonic sensor
        self.sensor = UltrasonicSensor(TRIG=23, ECHO=24)

    def move_forward(self):
        self.right_motor.move_forward()
        self.left_motor.move_forward()
        sleep(1)  # Move forward for a short duration
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
        self.angle = (self.angle + ANGLE_CHANGE) % 360

    def turn_right(self):
        self.angle = (self.angle - ANGLE_CHANGE) % 360

    def display_map(self):
        plt.figure(figsize=(10, 10))  # Set figure size
        plt.imshow(self.grid, cmap='Greys', origin='lower')
        plt.colorbar(label='Occupancy (1: Occupied, 0: Free)')
        plt.title('Occupancy Grid Map')
        plt.xlabel('Grid X Position')
        plt.ylabel('Grid Y Position')

        # Add grid lines
        plt.grid(color='blue', linestyle='--', linewidth=0.5)

        # Save the map as an image file
        plt.savefig('occupancy_grid_map.png', bbox_inches='tight', dpi=300)  # Save with high resolution
        plt.show()  # Show the saved map

    def run(self):
        try:
            while True:
                self.move_forward()
                self.update_map()
                # Optionally turn after a few moves to create a better map
                if np.random.rand() < 0.5:
                    self.turn_left()
                else:
                    self.turn_right()
                sleep(0.5)  # Delay between movements

        except KeyboardInterrupt:
            print("Stopping SLAM...")
            self.display_map()
            self.right_motor.stop_motor()
            self.left_motor.stop_motor()
            self.sensor.cleanup()

if __name__ == "__main__":
    GPIO.setwarnings(False)  # Disable warnings for GPIO
    slam = SLAM()
    slam.run()
