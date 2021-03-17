import RPi.GPIO as GPIO
import time

aux_vcc = 23
signal = 24
a = 1

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(signal, GPIO.IN) #, pull_up_down=GPIO.PUD_UP)
GPIO.setup(aux_vcc, GPIO.OUT)
GPIO.output(aux_vcc, GPIO.HIGH)

while True:
    a = GPIO.input(signal)
    print("status of a: ")
    print(a)
    if (a == False):
        print("Sensor is Working")
    else:
        print("Sensor is not working")
