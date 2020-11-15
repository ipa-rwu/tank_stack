#!/usr/bin/env python

import rospy

def main():
    rospy.init_node('tank_param')
    _pin_definition = rospy.get_param("/pin_definition_out", {})
    print(_pin_definition)
    _pin = {}
    for definition, pin in _pin_definition.items():
        if definition == "left_motor_forward":
            pin_left_forward = pin
            print(pin_left_forward)
        if not isinstance(pin, int):
            del _pin[pin]
        pin = int(pin)
        _pin[pin] = definition
    print(_pin)

    for key in _pin.keys():
        print(_pin[key])


if __name__ == "__main__":
    main()