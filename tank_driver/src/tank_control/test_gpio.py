#!/usr/bin/env python

import RPi.GPIO as GPIO
import os
import yaml

_FREQUENCY = 20
_MAX_PWM = 255
_MIN_PWM = 0
_LOW = 0
_HIGH = 1


def main():
    os.getcwd()
    os.chdir('../..')
    config_path = os.getcwd() + "/config/config.yaml"

    with open(config_path) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        config_yaml = yaml.load(file, Loader=yaml.FullLoader)

    _pin_definition = config_yaml["Definition"]
    print(_pin_definition)
    for item in _pin_definition:
        for pin in item:
            definition = item[pin]
    # Assign pins to motor
        if definition.find("left"):
            if definition.find("forward"):
                pin_left_forward = pin
            if definition.find("backward"):
                pin_left_backward = pin
            if definition.find("pwm"):
                pin_left_pwm = pin

        if definition.find("right"):
            if definition.find("forward"):
                pin_right_forward = pin

            if definition.find("backward"):
                pin_right_backward = pin
            if definition.find("pwm"):
                pin_right_pwm = pin

    pin_left_forward = 20
    pin_left_backward = 21
    pin_left_pwm = 19
    pin_right_forward = 26
    pin_right_backward = 16
    pin_right_pwm = 13

    print(pin_left_forward, pin_left_backward, pin_left_pwm, pin_right_forward, pin_right_backward, pin_right_pwm)

    # set gpio
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(pin_left_forward, GPIO.OUT)
    GPIO.setup(pin_left_backward, GPIO.OUT)


    GPIO.setup(pin_right_forward, GPIO.OUT)
    GPIO.setup(pin_right_backward, GPIO.OUT)

    pl = GPIO.PWM(pin_left_pwm, _FREQUENCY)
    pr = GPIO.PWM(pin_right_pwm, _FREQUENCY)

    while 1:
        GPIO.output(pin_left_forward, _HIGH)
        GPIO.output(pin_left_backward, _LOW)

        GPIO.output(pin_right_forward, _HIGH)
        GPIO.output(pin_right_backward, _LOW)

        speed = 100
        pl.start(speed)
        pr.start(speed)

if __name__ == '__main__':
    main()
    GPIO.cleanup()