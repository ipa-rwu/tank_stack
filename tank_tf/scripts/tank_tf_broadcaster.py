#!/usr/bin/env python  

import roslib

roslib.load_manifest('learning_tf')
import rospy
import tf

def handle_turtle_pose(msg, robotname):
    br = tf.TransformBroadcaster()
    br.sendTransform(
        (msg.x, msg.y, 0),
        tf.transformations.quaternion_from_euler(0, 0, msg.theta),
        rospy.Time.now(),
        robotname,
        "world")

if __name__ == '__main__':
    rospy.init_node('tank_tf_broadcaster')
    turtlename = rospy.get_param('~turtle')
    rospy.Subscriber('/%s/pose' % turtlename,
                        turtlesim.msg.Pose,
                        handle_turtle_pose,
                        turtlename)
    rospy.spin()