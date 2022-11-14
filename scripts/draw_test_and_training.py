#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import csv
import roslib

TRAINING_PATH = '/home/fmasa/catkin_ws/src/nav_cloning/data/result_with_dir_use_dl_output/20221115_02:58:36_training_2.0/training.csv'
TEST_PATH = '/home/fmasa/catkin_ws/src/nav_cloning/data/result_with_dir_use_dl_output/20221115_00:48:55_training_traditional/training.csv'

class draw_training_node:
    def __init__(self):
        rospy.init_node("draw_node", anonymous=True)
        # self.path = roslib.packages.get_pkg_dir('draw_nav_cloning') + '/data/analysis/'
        self.path_pub = rospy.Publisher('move_base/DWAPlannerROS/local_plan', Path, queue_size=10)
        self.path2_pub = rospy.Publisher('test_path', Path, queue_size=10)
        self.path_data = Path()
        self.path_data2 = Path()
        self.path_data.header.frame_id = "map"
        self.path_data2.header.frame_id = "map"
        self.make_path(self.path_data, TRAINING_PATH)
        self.make_path(self.path_data2, TEST_PATH)

    def make_path(self, path_data, PATH):
        with open(PATH, 'r') as f:
            is_first = True
            for row in csv.reader(f):
                if is_first:
                    is_first = False
                    continue
                str_step, str_mode, str_loss, str_angle_error, str_distance, str_x, str_y, str_the= row
                x, y, the = float(str_x), float(str_y), float(str_the)
                pose = PoseStamped()
                pose.header.frame_id = "map"
                pose.pose.position.x = x
                pose.pose.position.y = y
                path_data.poses.append(pose)

    def loop(self):
        self.path_pub.publish(self.path_data)
        self.path2_pub.publish(self.path_data2)
    
if __name__ == '__main__':
    rg = draw_training_node()
    r = rospy.Rate(1 / 0.5)
    while not rospy.is_shutdown():
        rg.loop()
        r.sleep()
