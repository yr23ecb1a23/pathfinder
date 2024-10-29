# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
class Motor:
    def __init__(self, inlet1, inlet2, enable, digital_frequency):
        self.inlet1 = inlet1
        self.inlet2 = inlet2
        self.enable = enable
        self.digital_frequency = digital_frequency
        GPIO.setup(self.inlet1, GPIO.OUT)
        GPIO.setup(self.inlet2, GPIO.OUT)
        GPIO.setup(self.enable,GPIO.OUT)
        GPIO.output(self.inlet1,GPIO.LOW)
        GPIO.output(self.inlet2,GPIO.LOW)
        self.pwm = GPIO.PWM(self.enable, self.digital_frequency)
        self.pwm.start(25)
    def motorStop(self):
        pass
    def moveForward(self):
        pass

    def moveReverse(self):
        pass

    def setMotorSpeed(self):
        pass
in1 = 23
in2 = 24
en = 25
temp1=1

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,100)

p.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")

while(1):

    x=input()

    if x=='r':
        print("run")
        if(temp1==1):
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            print("forward")
            x='z'
        else:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            print("backward")
            x='z'


    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='l':
        print("low")
        p.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(75)
        x='z'


    elif x=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break

    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
