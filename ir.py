import RPi.GPIO as GPIO
import time

aux_vcc = 16
signal = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(signal, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(aux_vcc, GPIO.OUT)
GPIO.output(aux_vcc, GPIO.HIGH)

def loop():
	a = GPIO.input(signal)
	if (a == False):
		print("Sensor is Working")
	else:
		print("Sensor is not working")

loop()