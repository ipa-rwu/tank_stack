#!/usr/bin/env python

from motor_control import MotorGPIO
import yaml
import os

def main():
    # motor = MotorGPIO()
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

        print(pin)
        print(definition)
    # Assign pins to motor
    # !!!!!!! wrong!!!!!!!!!
        if definition.find("left_motor_forward"):
            pin_left_forward = pin
        if definition.find("left_motor_backward"):
            pin_left_backward = pin
        if definition.find("left_motor_pwm"):
            pin_left_pwm = pin

        if definition.find("right_motor_forward"):
            pin_right_forward = pin

        if definition.find("right_motor_backward"):
            pin_right_backward = pin
        if definition.find("right_motor_pwm"):
            pin_right_pwm = pin

    pin_left_forward = 20
    pin_left_backward = 21
    pin_left_pwm = 16
    pin_right_forward = 19
    pin_right_backward = 26
    pin_right_pwm = 13

    print(pin_left_forward, pin_left_backward, pin_left_pwm, pin_right_forward, pin_right_backward, pin_right_pwm)
    left_motor = MotorGPIO(pin_left_forward, pin_left_backward, pin_left_pwm)
    right_motor = MotorGPIO(pin_right_forward, pin_right_backward, pin_right_pwm)
    left_speed_percent = 0
    right_speed_percent = 0

    while True:
        left_speed_percent = 5
        right_speed_percent = 5
        left_motor.move(left_speed_percent)
        right_motor.move(right_speed_percent)  



if __name__ == '__main__':
    main()
    GPIO.cleanup()