#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import csv
import roslib

class draw_training_node:
    def __init__(self):
        rospy.init_node("draw_node", anonymous=True)
        self.path = roslib.packages.get_pkg_dir('nav_cloning') + '/data/analysis/'
        self.path_pub = rospy.Publisher('move_base/DWAPlannerROS/local_plan', Path, queue_size=10)
        self.path_data = Path()
        self.path_data.header.frame_id = "map"
        self.make_path()

    def make_path(self):
        with open(self.path + 'training.csv', 'r') as f:
            is_first = True
            for row in csv.reader(f):
                if is_first:
                    is_first = False
                    continue
                str_step, str_mode, str_loss, str_angle_error, str_distance, str_x, str_y, str_the, direction_ = row
                x, y, the = float(str_x), float(str_y), float(str_the)
                pose = PoseStamped()
                pose.header.frame_id = "map"
                pose.pose.position.x = x
                pose.pose.position.y = y
                self.path_data.poses.append(pose)

    def loop(self):
        self.path_pub.publish(self.path_data)
    
if __name__ == '__main__':
    rg = draw_training_node()
    r = rospy.Rate(1 / 0.5)
    while not rospy.is_shutdown():
        rg.loop()
        r.sleep()
