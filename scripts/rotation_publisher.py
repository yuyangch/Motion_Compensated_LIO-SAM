import math

import rospy
from sensor_msgs.msg import Imu
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import Header
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32
from visualization_msgs.msg import Marker
from scipy.spatial.transform import Rotation as R
#std_msgs/Float32
from nav_msgs.msg import Odometry
from copy import deepcopy
import numpy as np
import struct
class Nodo(object):
    def __init__(self):
        # Params
        #self.image = None
        #self.br = CvBridge()
        # Node cycle rate (in Hz).
        #self.loop_rate = rospy.Rate(1)
        #rospy.init_node()
        #self.imuPub = rospy.Publisher('/iris/vel_cmd', Imu, queue_size=1)
        #self.posPub = rospy.Publisher('/pos', PoseStamped, queue_size=1)

        self.position=[0.0,0.0,0.0]
        self.orientation=[1.0,0.0,0.0,0.0]
        self.marker_id=0
        self.corner_feature_points_list=[]
        self.corner_feature_mean=np.matrix([0.0,0.0,0.0])
        self.corner_feature_mean_list=[]
        self.robot_slam_pose_sub=rospy.Subscriber('/odometry/imu',Odometry,self.odometry_callback,queue_size=1)
        self.pointcloud2sub=rospy.Subscriber('/lio_sam/feature/cloud_corner',PointCloud2,self.corner_feature_callback,queue_size=1)
        rospy.init_node('helper_Imu_modfiying_node', anonymous=True)
        pub = rospy.Publisher('/iris/vel_cmd', Vector3, queue_size=10)
        self.marker_pub=rospy.Publisher('/corner_feature_mean',Marker,queue_size=2)
        self.corner_feature_mean_list_sum=np.matrix([0.0,0.0,0.0]).transpose()


	    #rospy.init_node('talker', anonymous=True)
        rate = rospy.Rate(10) # 10hz
        count=0
        #rospy.spin()
        
        while not rospy.is_shutdown():
            #azimuth=np.random.normal(0, 6.0)
            #elevation=np.random.normal(0, 6.0)
            azimuth=self.aim_at_mean_center_of_all_features()
            #azimuth=0.0
            elevation=0.0
            data=Vector3()            
            data.z=azimuth  #azimuth
            data.y=elevation  #elevation
	        #data.z=3.0
	        #hello_str = "hello world %s" % rospy.get_time()
	        #rospy.loginfo(hello_str)
            pub.publish(data)
            #test rotated center
            r = R.from_euler('z', azimuth, degrees=True)
            R__=r.as_matrix()
            camera_center=np.matrix([5.0,0.0,0.0]).transpose()
            camera_center=R__*camera_center
            #change to world frame
            r = R.from_quat(self.orientation)
            R_=r.as_matrix()
            camera_center=R_*camera_center+np.matrix(self.position).transpose()       
            self.publish_marker(camera_center[0,0],camera_center[1,0],camera_center[2,0],"blue",2)
            rate.sleep()
        

    def aim_at_mean_center_of_all_features(self):
        #p_c=R^T(point-t)
        #R
        r = R.from_quat(self.orientation)
        R_=r.as_matrix()
        R_T=R_.transpose()
        #point --3x1 matrix
        #point_w=self.corner_feature_mean.transpose()
        point_w=self.corner_feature_mean_list_sum
        #t 
        t=np.matrix(self.position).transpose()

        #p_c camera frame
        p_c=R_T*(point_w-t)
        x=p_c[0,0]
        y=p_c[1,0]
        theta=np.arctan2(y, x) * 180.0 / np.pi
        return theta
        #p_c



        #theta=atan2(pc_y,pc_x)



    def publish_marker(self,x,y,z,color,markerid):
        marker=Marker()
        marker.header.frame_id = "map";
        marker.header.stamp = rospy.Time.now();

        marker.id = markerid;
        marker.type = 2;#Sphere
        marker.action = 0;#ADD
        marker.pose.position.x = x;
        marker.pose.position.y = y;
        marker.pose.position.z = z;
        marker.pose.orientation.x = 0.0;
        marker.pose.orientation.y = 0.0;
        marker.pose.orientation.z = 0.0;
        marker.pose.orientation.w = 1.0;
        marker.scale.x = 5.0;
        marker.scale.y = 5.0;
        marker.scale.z = 5.0;
        if color == "red":
            marker.color.r = 1.0;
            marker.color.g = 0.0;
            marker.color.b = 0.0;
        elif color == "green":
            marker.color.r = 0.0;
            marker.color.g = 1.0;
            marker.color.b = 0.0;
        elif color == "blue":
            marker.color.r = 0.0;
            marker.color.g = 0.0;
            marker.color.b = 1.0;        
        marker.color.a = 1.0;

        self.marker_pub.publish(marker)        


    def corner_feature_callback(self,data): #calculate corner feature mean
        self.corner_feature_points_list=[]
        feature_sum=np.matrix([0.0,0.0,0.0])
        for i in range (0,data.width):
            xyz=[]
            for j in range (0,3):
                float_=struct.unpack('<f', struct.pack('4B', *data.data[i*32+j*4:i*32+j*4+4]))
                #print("float",float_[0])
                xyz.append(float_[0])
            self.corner_feature_points_list.append(xyz.copy())
            if i==1:
                print("xyz",xyz)
            #print("feature_sum",feature_sum)
            feature_sum+=np.matrix(xyz)
        feature_sum=feature_sum*(1.0/data.width)
        r = R.from_quat(self.orientation)
        R_=r.as_matrix()
        feature_sum=R_*feature_sum.transpose()+np.matrix(self.position).transpose()
        print("feature_sum mean",feature_sum)
        self.corner_feature_mean=feature_sum.copy()
        self.corner_feature_mean_list.append(feature_sum.copy())
        self.corner_feature_mean_list_sum=np.matrix([0.0,0.0,0.0]).transpose()
        for i in range (0,len(self.corner_feature_mean_list)):
            self.corner_feature_mean_list_sum+=self.corner_feature_mean_list[i]
        self.corner_feature_mean_list_sum=self.corner_feature_mean_list_sum*(1.0/len(self.corner_feature_mean_list))
        self.publish_marker(self.corner_feature_mean[0,0],self.corner_feature_mean[1,0],self.corner_feature_mean[2,0],"green",0)
        self.publish_marker(self.corner_feature_mean_list_sum[0,0],self.corner_feature_mean_list_sum[1,0],self.corner_feature_mean_list_sum[2,0],"red",1)
        #publish
    def odometry_callback(self,data): #register current robot pose
        x=data.pose.pose.position.x
        y=data.pose.pose.position.y
        z=data.pose.pose.position.z

        quat_x=data.pose.pose.orientation.x
        quat_y=data.pose.pose.orientation.y
        quat_z=data.pose.pose.orientation.z
        quat_w=data.pose.pose.orientation.w
        self.position=[x,y,z].copy()
        self.orientation=[quat_x,quat_y,quat_z,quat_w].copy()

if __name__ == '__main__':
    my_node = Nodo()
    #my_node.start()
