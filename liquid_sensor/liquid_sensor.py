import RPi.GPIO as GPIO
import time

def liquid_sensor(sensor):
    # high_pin = 23

    GPIO.setup(sensor, GPIO.IN)

    sens_high = GPIO.input()
    if sens_high:
        print("high")
    else:
        print("low")

    time.sleep(1)
    return sens_high        # 1 means high