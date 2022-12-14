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



class Nodo(object):

    def __init__(self,name):
        self.gt_position=[]
        self.gt_orientation=[]
        self.slam_position=[]
        self.slam_orientation=[]
        self.position_error=[]
        self.orientation_error=[]
        self.f=open(name+".csv",'a+')
        self.posPub = rospy.Publisher('/odom_error', Vector3, queue_size=1)
        rospy.init_node('helper_odometry_error_node', anonymous=True)
        self.slam_odom_Sub=rospy.Subscriber('/lio_sam/mapping/odometry', Odometry,self.slam_odom_callback,queue_size=1)
        self.gt_odom_Sub=rospy.Subscriber('/body_pose_ground_truth', Odometry,self.gt_odom_callback,queue_size=10)
        rospy.spin()

    def append_error(self):
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
    def slam_odom_callback(self,data):
        self.slam_position=[data.pose.pose.position.x,data.pose.pose.position.y,data.pose.pose.position.z].copy()
        self.slam_orientation=[data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w].copy()
        self.append_error()

if __name__ == '__main__':
    filename=sys.argv[1]
    my_node = Nodo(filename)
    #my_node.start()
    