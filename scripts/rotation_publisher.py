import math

import rospy
from sensor_msgs.msg import Imu
from std_msgs.msg import Header
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32

#std_msgs/Float32
from copy import deepcopy
import numpy as np

class Nodo(object):
    def __init__(self):
        # Params
        #self.image = None
        #self.br = CvBridge()
        # Node cycle rate (in Hz).
        #self.loop_rate = rospy.Rate(1)

        #rospy.init_node()s

        #self.imuPub = rospy.Publisher('/iris/vel_cmd', Imu, queue_size=1)
        #self.posPub = rospy.Publisher('/pos', PoseStamped, queue_size=1)
        rospy.init_node('helper_Imu_modfiying_node', anonymous=True)
        pub = rospy.Publisher('/iris/vel_cmd', Vector3, queue_size=10)
	    #rospy.init_node('talker', anonymous=True)
        rate = rospy.Rate(10) # 10hz
        count=0
        while not rospy.is_shutdown():
            azimuth=np.random.normal(0, 3.0)
            elevation=np.random.normal(0, 3.0)
            data=Vector3()            
            data.z=azimuth  #azimuth
            data.y=elevation  #elevation
	        #data.z=3.0
	        #hello_str = "hello world %s" % rospy.get_time()
	        #rospy.loginfo(hello_str)
            pub.publish(data)
            rate.sleep()



    def imucallback(self,data):
        
        self.Imu_=deepcopy(data)
        self.Imu_.linear_acceleration.z=self.Imu_.linear_acceleration.z+9.80511
        self.imuPub.publish(self.Imu_)
    def poscallback(self,data):
        self.PoseStamped_=deepcopy(data)

if __name__ == '__main__':
    my_node = Nodo()
    #my_node.start()
