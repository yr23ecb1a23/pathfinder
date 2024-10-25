import time
import board
import busio
import adafruit_mpu6050

# Create I2C object using the appropriate pins
i2c = busio.I2C(board.SCL, board.SDA)

# Create the MPU6050 object
mpu = adafruit_mpu6050.MPU6050(i2c)

# Read and print accelerometer and gyroscope data
while True:
    # Accelerometer data
    print("Accelerometer: X={:.2f}, Y={:.2f}, Z={:.2f} m/s^2".format(mpu.acceleration[0],
                                                                     mpu.acceleration[1], mpu.acceleration[2]), end='\r')

    # Gyroscope data
    #print("Gyroscope: X={:.2f}, Y={:.2f}, Z={:.2f} rad/s".format(
    #mpu.gyro[0], mpu.gyro[1], mpu.gyro[2]))

    # Temperature data
    #print("Temperature: {:.2f} C".format(mpu.temperature))

    # Add a short delay before reading the next set of values
    time.sleep(0.2)
