#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO

from motor_control import MotorGPIO


GPIO.setmode(GPIO.BCM)

_MAX_PWM = 255
_MIN_PWM = 0


class TankControl:

    def __init__(self):

        rospy.init_node('tank_control', log_level=rospy.DEBUG)

        # Pin numbers are the GPIO# value, not the literal pin number.
        self._pin_definition = rospy.get_param("~Definition", {})

        for pin, definition in self._pin_definition.items():
            if not isinstance(pin, int):
                del self._pin_definition[pin]
            pin = int(pin)
            self._pin_definition[pin] = definition

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

        self._left_motor = MotorGPIO(pin_left_forward, pin_left_backward, pin_left_pwm)
        self._right_motor = MotorGPIO(pin_right_forward, pin_right_backward, pin_right_pwm)
        self._left_speed_percent = 0
        self._right_speed_percent = 0


        self._last_received = rospy.get_time()
        self._timeout = rospy.get_param('~timeout', "2")
        self._rate = rospy.get_param('~rate', "50")
        self._max_speed = rospy.get_param('~max_speed', "0.5")
        self._wheel_base = rospy.get_param('~wheel_base', "0.091")
        self._cmd_vel_topic = rospy.get_param('~cmd_vel', 'cmd_vel')

        # These states will be set to pins right before the node shuts down.
        self._shutdown_states = rospy.get_param("~shutdown_states", {})

        # Set default states.
        self._start_states = rospy.get_param("~states", {})



        for pin, state in self.states.items():
            if not isinstance(pin, int):
                del self.states[pin]
            pin = int(pin)
            self._start_statesstates[pin] = state


        for pin, state in self._shutdown_states.items():
            if not isinstance(pin, int):
                del self._shutdown_states[pin]
            pin = int(pin)
            self._shutdown_states[pin] = state

    def velocity_received_callback(self, message):
        """Handle new velocity command message."""

        self._last_received = rospy.get_time()

        # Extract linear and angular velocities from the message
        linear = message.linear.x
        angular = message.angular.z

        # Calculate wheel speeds in m/s
        left_speed = linear - angular*self._wheel_base/2
        right_speed = linear + angular*self._wheel_base/2

        # Ideally we'd now use the desired wheel speeds along
        # with data from wheel speed sensors to come up with the
        # power we need to apply to the wheels, but we don't have
        # wheel speed sensors. Instead, we'll simply convert m/s
        # into percent of maximum wheel speed, which gives us a
        # duty cycle that we can apply to each motor.
        self._left_speed_percent = (
            100 * left_speed/self._max_speed)
        self._right_speed_percent = (
            100 * right_speed/self._max_speed)

    def shutdown(self):

        # Reset pin state.
        rospy.loginfo("Reseting pin states...")
        for pin, state in self._shutdown_states.iteritems():
            GPIO.output(pin, state)
        self._pwm.start(0)

    def run(self):
        """The control loop of the driver."""
        # Cleanup when termniating the node
        rospy.on_shutdown(self.shutdown)

        # Overall loop rate: should be faster than fastest sensor rate
        r = rospy.Rate(self._rate)

        # Setup subscriber for velocity twist message
        rospy.Subscriber(
            self._cmd_vel_topic, Twist, self.velocity_received_callback)

        # Start polling the sensors and base controller
        while not rospy.is_shutdown():
            # If we haven't received new commands for a while, we
            # may have lost contact with the commander-- stop
            # moving
            delay = rospy.get_time() - self._last_received
            if delay < self._timeout:
                self._left_motor.move(self._left_speed_percent)
                self._right_motor.move(self._right_speed_percent)
            else:
                self._left_motor.move(0)
                self._right_motor.move(0)
            # now = rospy.Time.now()

            r.sleep()

def main():
    driver = TankControl()

    # Run driver. This will block
    driver.run()


if __name__ == '__main__':
    main()
