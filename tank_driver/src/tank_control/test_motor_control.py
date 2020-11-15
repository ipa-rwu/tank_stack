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

    left_motor = MotorGPIO(pin_left_forward, pin_left_backward, pin_left_pwm)
    right_motor = MotorGPIO(pin_right_forward, pin_right_backward, pin_right_pwm)
    left_speed_percent = 0
    right_speed_percent = 0

    left_motor.move(left_speed_percent)
    right_motor.move(right_speed_percent)


if __name__ == '__main__':
    main()