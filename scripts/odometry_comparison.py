import math

import rospy
from sensor_msgs.msg import Imu
from std_msgs.msg import Header
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry

import numpy as np
from copy import deepcopy

from scipy.spatial.transform import Rotation as R
import sys
import time
import copy

class Nodo(object):

    def __init__(self,name):
        self.gt_position=[]
        self.gt_orientation=[]
        self.slam_position=[]
        self.slam_orientation=[]
        self.position_error=[]
        self.orientation_error=[]
        self.slam_position_record=[]
        self.slam_orientation_record=[]
        self.gt_position_record=[]
        self.gt_orientation_record=[]
        self.relative_position_pair_index_list=[]
        self.relative_length_list=[10,20,40,60,80,100]
        self.gt_position_diff_norm_sum=0.000000001
        self.position_error_sum=0
        self.orientation_error_sum=0
        self.live_counter=0
        self.prev_counter=10000
        self.time_checkpoint=time.time()
        self.f=open(name+".csv",'w+')
        self.posPub = rospy.Publisher('/odom_error', Vector3, queue_size=1)
        rospy.init_node('helper_odometry_error_node', anonymous=True)
        self.slam_odom_Sub=rospy.Subscriber('/lio_sam/mapping/odometry', Odometry,self.slam_odom_callback,queue_size=1)
        self.gt_odom_Sub=rospy.Subscriber('/body_pose_ground_truth', Odometry,self.gt_odom_callback,queue_size=10)
        self.f.write("gt_x,gt_y,gt_z,slam_x,slam_y,slam_z\n")
        rospy.spin()

    def record_poses(self): #append error 
        #print (self.slam_position.shape)
        #if self.slam_position.shape is not (1,3):
        #    return
        self.slam_position_record.append((self.slam_position).copy())
        self.gt_position_record.append((self.gt_position).copy())
        self.f.write(str(self.gt_position[0])+','+str(self.gt_position[1])+','+str(self.gt_position[2])+',')        
        self.f.write(str(self.slam_position[0])+','+str(self.slam_position[1])+','+str(self.slam_position[2])+'\n')

    def gt_odom_callback(self,data):
        self.gt_position=[data.pose.pose.position.x,data.pose.pose.position.y,data.pose.pose.position.z].copy()
        self.gt_orientation=[data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w].copy()
        self.live_counter+=1
    def slam_odom_callback(self,data):
        self.slam_position=[data.pose.pose.position.x,data.pose.pose.position.y,data.pose.pose.position.z].copy()
        self.slam_orientation=[data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w].copy()
        self.live_counter+=1
        self.record_poses()
        #self.append_error()


if __name__ == '__main__':
    filename=sys.argv[1]
    my_node = Nodo(filename)
    #my_node.start()
    