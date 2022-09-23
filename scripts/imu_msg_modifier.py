import math

import rospy
from sensor_msgs.msg import Imu
from std_msgs.msg import Header
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import PoseStamped



from copy import deepcopy



class Nodo(object):
    def __init__(self):
        # Params
        #self.image = None
        #self.br = CvBridge()
        # Node cycle rate (in Hz).
        #self.loop_rate = rospy.Rate(1)

        #rospy.init_node()s

        self.imuPub = rospy.Publisher('/imu_raw', Imu, queue_size=1)
        #self.posPub = rospy.Publisher('/pos', PoseStamped, queue_size=1)
        rospy.init_node('helper_Imu_modfiying_node', anonymous=True)

        self.imuSub=rospy.Subscriber('/gazebo_ros_imu', Imu,self.imucallback,queue_size=1)
        #self.posSub=rospy.Subscriber('/OpticFlow', PoseStamped,self.poscallback,queue_size=1)
        #rospy.Subscriber("/camera/image_color",Image,self.callback)
        #Data Memory
        rospy.spin()


    def imucallback(self,data):
        
        self.Imu_=deepcopy(data)
        self.Imu_.linear_acceleration.z=self.Imu_.linear_acceleration.z+9.80511
        self.imuPub.publish(self.Imu_)
    def poscallback(self,data):
        self.PoseStamped_=deepcopy(data)

if __name__ == '__main__':
    my_node = Nodo()
    #my_node.start()
