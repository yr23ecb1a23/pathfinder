
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
        self.pwm.start(25 + speed_offset)

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
        self.pwm.ChangeDutyCycle(speed + self.speed_offset)
        return True



