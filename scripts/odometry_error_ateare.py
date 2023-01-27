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
        self.f=open(name+".csv",'a+')
        self.posPub = rospy.Publisher('/odom_error', Vector3, queue_size=1)
        rospy.init_node('helper_odometry_error_node', anonymous=True)
        self.slam_odom_Sub=rospy.Subscriber('/lio_sam/mapping/odometry', Odometry,self.slam_odom_callback,queue_size=1)
        self.gt_odom_Sub=rospy.Subscriber('/body_pose_ground_truth', Odometry,self.gt_odom_callback,queue_size=10)
        while True:
            if time.time()-self.time_checkpoint<3:
                continue
            if self.prev_counter==self.live_counter:
                break
            self.prev_counter=copy.deepcopy(self.live_counter)
            self.time_checkpoint=time.time()
        self.sample_relative_pose_pairs()
        self.calculate_ATE_ARE_errors()


    def record_poses(self): #append error 
        #print (self.slam_position.shape)
        #if self.slam_position.shape is not (1,3):
        #    return

        self.slam_position_record.append((self.slam_position).copy())
        self.gt_position_record.append((self.gt_position).copy())

        #position_error=np.matrix(self.slam_position)-np.matrix(self.gt_position)
        #orientation_error=np.matrix(self.slam_orientation)-np.matrix(self.gt_orientation)
        gt_r=R.from_quat(self.gt_orientation)
        gt_rpy=gt_r.as_euler('xyz',degrees=True)
        gt_yaw=gt_rpy[2]
        slam_r=R.from_quat(self.slam_orientation)
        slam_rpy=slam_r.as_euler('xyz',degrees=True)
        slam_yaw=slam_rpy[2]

        self.gt_orientation_record.append(gt_yaw.copy())
        self.slam_orientation_record.append(slam_yaw.copy())

    def sample_relative_pose_pairs(self):
        #all consecutive relative pairs
        for i in range (0,len(self.gt_position_record)-1):
            #self.relative_position_pair_index_list
            self.relative_position_pair_index_list.append((i,i+1))
        #all random relative pairs with distance [10,100,50]
        for length in self.relative_length_list:
            for i in range (0,len(self.gt_position_record)-1):
                for j in range (i,len(self.gt_position_record)-1):
                    relative_distance=np.matrix(self.gt_position_record[j])-np.matrix(self.gt_position_record[i])
                    if np.linalg.norm(relative_distance)>length:
                        self.relative_position_pair_index_list.append((i,j))
                        break
        for pair in self.relative_position_pair_index_list:
            print(pair)
    def calculate_ATE_ARE_errors(self):
        for pair in self.relative_position_pair_index_list:
            self.calculate_pairwise_errors(pair[0],pair[1])
        ATE=self.position_error_sum/self.gt_position_diff_norm_sum
        ARE=self.orientation_error_sum/self.gt_position_diff_norm_sum
        self.f.write(str(ATE)+','+str(ARE)+'\n')
        #print()
    def calculate_pairwise_errors(self,i,j):
        gt_position_diff=np.matrix(self.gt_position_record[i])-np.matrix(self.gt_position_record[j])
        slam_position_diff=np.matrix(self.slam_position_record[i])-np.matrix(self.slam_position_record[j])
        position_error=gt_position_diff-slam_position_diff
        print("gt_position_diff",gt_position_diff)
        print("slam_position_diff",slam_position_diff)
        print("position_error",position_error)
        self.gt_position_diff_norm_sum+=np.linalg.norm(gt_position_diff)
        self.position_error_sum+=np.linalg.norm(position_error)

        #gt_r=R.from_quat(self.gt_orientation_record[i])
        #gt_rpy=gt_r.as_euler('xyz',degrees=True)
        gt_yaw=self.gt_orientation_record[i]

        #gt_r_=R.from_quat(self.gt_orientation_record[j])
        #gt_rpy_=gt_r_.as_euler('xyz',degrees=True)
        gt_yaw_=self.gt_orientation_record[j]

        #slam_r=R.from_quat(self.slam_orientation_record[i])
        #slam_rpy=slam_r.as_euler('xyz',degrees=True)
        slam_yaw=self.slam_orientation_record[i]      

        #slam_r_=R.from_quat(self.slam_orientation_record[j])
        #slam_rpy_=slam_r_.as_euler('xyz',degrees=True)
        slam_yaw_=self.slam_orientation_record[j]


        gt_yaw_diff=gt_yaw_-gt_yaw
        slam_yaw_diff=slam_yaw_-slam_yaw
        orientation_error=abs(gt_yaw_diff-slam_yaw_diff)
        print("gt_yaw_diff",gt_yaw_diff)
        print("slam_yaw_diff",slam_yaw_diff)
        print("orientation_error",orientation_error)


        self.orientation_error_sum+=orientation_error


    def append_error(self): #append error 
        position_error=np.matrix(self.slam_position)-np.matrix(self.gt_position)
        #orientation_error=np.matrix(self.slam_orientation)-np.matrix(self.gt_orientation)
        gt_r=R.from_quat(self.gt_orientation)
        gt_rpy=gt_r.as_euler('xyz',degrees=True)
        gt_yaw=gt_rpy[2]
        slam_r=R.from_quat(self.slam_orientation)
        slam_rpy=slam_r.as_euler('xyz',degrees=True)
        slam_yaw=slam_rpy[2]
        self.position_error.append((np.linalg.norm(position_error)).copy())
        self.orientation_error.append((np.fabs(slam_yaw-gt_yaw)).copy())
        v3=Vector3()

        v3.x=sum(self.position_error)/len(self.position_error)
        v3.y=sum(self.orientation_error)/len(self.orientation_error)
        self.f.write(str(v3.x)+','+str(v3.y)+'\n')
        self.posPub.publish(v3)
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
    