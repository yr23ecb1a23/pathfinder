import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for TRIG and ECHO
TRIG = 4
ECHO = 5

# Set up the GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

try:
    while True:
        # Set TRIG to LOW

        # Set TRIG to HIGH for 10 microseconds
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
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

        print(f"Distance: {distance:.2f} cm", end='\r')

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
