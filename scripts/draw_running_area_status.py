#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
from visualization_msgs.msg import *
import csv
import roslib

RADIUS = 0.03

class draw_training_node:
    def __init__(self):
        rospy.init_node("draw_node", anonymous=True)
        self.path = roslib.packages.get_pkg_dir('nav_cloning') + '/data/result_use_dl_output/20221213_00:51:03/'
        # self.path = roslib.packages.get_pkg_dir('nav_cloning') + '/data/analysis/use_dl_output/'
        self.path_pub = rospy.Publisher('move_base/DWAPlannerROS/local_plan', Path, queue_size=10)
        self.points1_pub = rospy.Publisher('point1', MarkerArray, queue_size=10)
        self.points2_pub = rospy.Publisher('point2', MarkerArray, queue_size=10)
        self.points3_pub = rospy.Publisher('point3', MarkerArray, queue_size=10)
        self.points4_pub = rospy.Publisher('point4', MarkerArray, queue_size=10)
        self.points5_pub = rospy.Publisher('point5', MarkerArray, queue_size=10)
        self.points6_pub = rospy.Publisher('point6', MarkerArray, queue_size=10)
        self.path_data = Path()
        self.points1 = MarkerArray()
        self.points2 = MarkerArray()
        self.points3 = MarkerArray()
        self.points4 = MarkerArray()
        self.points5 = MarkerArray()
        self.points6 = MarkerArray()
        self.point1_count = 0
        self.point2_count = 0
        self.point3_count = 0
        self.point4_count = 0
        self.point5_count = 0
        self.point6_count = 0
        self.path_data.header.frame_id = "map"
        self.pose_list = [[],[]]
        self.make_path()
        self.make_points()
        

    def make_path(self):
        # with open(self.path + 'training.csv', 'r') as f:
        with open(self.path + 'traceable_pos.csv', 'r') as f:
            is_first = True
            for row in csv.reader(f):
                # if is_first:
                #     is_first = False
                #     continue
                # str_step, str_mode, str_loss, str_angle_error, str_distance, str_x, str_y, str_the, direction_ = row
                # str_x, str_y, str_the, direction_ = row
                str_x, str_y, str_the = row
                x, y, the = float(str_x) + 100, float(str_y) + 100, float(str_the)
                pose = PoseStamped()
                pose.header.frame_id = "map"
                pose.pose.position.x = x
                pose.pose.position.y = y
                self.pose_list[0].append(x)
                self.pose_list[1].append(y)
                if len(self.pose_list[0]) %7 == 4:
                    self.path_data.poses.append(pose)
    
    def make_points(self):
        self.points1.markers = []
        self.points2.markers = []
        self.points3.markers = []
        self.points4.markers = []
        self.points5.markers = []
        self.points6.markers = []
        num = 0

        with open(self.path + 'result/score.csv', 'r') as f:
        # with open('/home/kiyooka/Downloads/first/score.csv', 'r') as f:
            for row in csv.reader(f):
                if (num+1) %7 != 4:
                    x = self.pose_list[0][num]
                    y = self.pose_list[1][num]
                else:
                    num += 1
                    x = self.pose_list[0][num]
                    y = self.pose_list[1][num]
                num += 1
                # str_x, str_y, str_score = row
                angle_score, position_score = row
                # x, y, score = float(str_x), float(str_y), float(str_score)
                score = float(position_score)

                point_marker = Marker()

                point_marker.header.frame_id = "map"
                point_marker.type = Marker.CYLINDER
                point_marker.action = point_marker.ADD

                point_marker.scale.x = 2 * RADIUS
                point_marker.scale.y = 2 * RADIUS
                point_marker.scale.z = 0.01

                point_marker.color.a = 1.0

                point_marker.pose.position.x = x #x
                point_marker.pose.position.y = y #y
                point_marker.pose.position.z = 0.0

                point_marker.pose.orientation.x = 0.0
                point_marker.pose.orientation.y = 0.0
                point_marker.pose.orientation.z = 0.0
                point_marker.pose.orientation.w = 1.0

                if score == 1.0:
                    point_marker.color.r = 1.0
                    point_marker.color.g = 0.0
                    point_marker.color.b = 0.0
                    point_marker.id = self.point1_count
                    self.point1_count += 1
                    self.points1.markers.append(point_marker)

                elif score >= 0.8:
                    point_marker.color.r = 0.0
                    point_marker.color.g = 1.0
                    point_marker.color.b = 0.0
                    point_marker.id = self.point2_count
                    self.point2_count += 1
                    self.points2.markers.append(point_marker)
                elif score >= 0.6:
                    point_marker.color.r = 0.0
                    point_marker.color.g = 0.0
                    point_marker.color.b = 1.0
                    point_marker.id = self.point3_count
                    self.point3_count += 1
                    self.points3.markers.append(point_marker)
                elif score >= 0.4:
                    point_marker.color.r = 1.0
                    point_marker.color.g = 0.0
                    point_marker.color.b = 1.0
                    point_marker.id = self.point4_count
                    self.point4_count += 1
                    self.points4.markers.append(point_marker)
                elif score >= 0.2:
                    point_marker.color.r = 1.0
                    point_marker.color.g = 1.0
                    point_marker.color.b = 0.0
                    point_marker.id = self.point5_count
                    self.point5_count += 1
                    self.points5.markers.append(point_marker)
                else:
                    point_marker.color.r = 1.0
                    point_marker.color.g = 1.0
                    point_marker.color.b = 0.0
                    point_marker.id = self.point6_count
                    self.point6_count += 1
                    self.points6.markers.append(point_marker)

    def loop(self):
        self.path_pub.publish(self.path_data)
        self.points1_pub.publish(self.points1)
        self.points2_pub.publish(self.points2)
        self.points3_pub.publish(self.points3)
        self.points4_pub.publish(self.points4)
        self.points5_pub.publish(self.points5)
        self.points6_pub.publish(self.points6)
    
if __name__ == '__main__':
    rg = draw_training_node()
    r = rospy.Rate(1 / 0.5)
    while not rospy.is_shutdown():
        rg.loop()
        r.sleep()
