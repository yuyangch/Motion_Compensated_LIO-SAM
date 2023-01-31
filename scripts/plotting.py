import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
#plt.style.use('seaborn-whitegrid')
#both figure 8,9 are in here, fig 8 is plotter_CU_C, fig 9 is plotter
class Plotter_C_UC(object):
	def __init__(self):
		self.file_num_initials=[2,3,4,5,6,7,8] #cut off at 8, data available at 12
		self.odom_error_pos=[]
		self.odom_error_rot=[]
		self.odom_error_pos_UC=[]
		self.odom_error_rot_UC=[]		
		self.file_affix='_sigma_kitti.csv'
		self.UC_file_affix='_sigma_kitti.csv'
		self.plot_rot=False
		self.read_files()
		self.read_files_UC()
		self.plot()
		
	def read_files(self):
		for i in self.file_num_initials:
			f=open("./input/"+str(i)+self.file_affix,"r")
			data = f.readlines()
			last_row=data[-1].split(',')
			self.odom_error_pos.append(float(last_row[0].strip('"')))
			self.odom_error_rot.append(float(last_row[1].strip('"')))
		
	def read_files_UC(self):
		for i in self.file_num_initials:
			f=open("./input_UC/"+str(i)+self.UC_file_affix,"r")
			data = f.readlines()
			last_row=data[-1].split(',')
			self.odom_error_pos_UC.append(float(last_row[0].strip('"')))
			self.odom_error_rot_UC.append(float(last_row[1].strip('"')))

	def plot(self):
		fig, ax1 = plt.subplots()
		if self.plot_rot==True:
			ax2 = ax1.twinx()
		#ax3 = ax1.twinx()
		#ax4 = ax1.twinx()		
		#fig=plt.figure()
		#ax=plt.axes()
		ax1.plot(self.file_num_initials,self.odom_error_pos,'r',label="Ours")
		if self.plot_rot==True:
			ax2.plot(self.file_num_initials,self.odom_error_rot,'b',label="Rotation Error")
			ax2.plot(self.file_num_initials,self.odom_error_rot_UC,'b-.',label="UC Rotation Error")
			ax2.legend( loc=1,fontsize = 'small', fancybox = True)
			ax2.set_ylabel('Yaw Erorr (degree/m)', color='b')
		ax1.plot(self.file_num_initials,self.odom_error_pos_UC,'r-.',label="LIO-SAM")


		ax1.legend( loc=2,fontsize = 'small', fancybox = True)

		plt.title("Input Standard Deviation vs Odom Error, Compensated vs Uncompensated")
		plt.xlabel("Control Input Standard Deviation")
		#plt.ylabel("Position Error ()")
		ax1.set_ylabel('Average Translation Error (%)', color='r')
		ax1.set_xlabel('Input Standard Deviation (degree)')
		plt.savefig('input_sigma_vs_odometry_error_C_UC_ateare.pdf')
		#plt.show()



class Plotter_IMU(object):
	def __init__(self):
		self.file_num_initials=[1,2,4,8,16] #cut off at 1.6 , data available at 3.2, need 6,10,12,14
		self.odom_error_pos=[]
		self.odom_error_rot=[]
		self.file_affix='x_imu.csv'
		self.read_files()
		self.plot()
	def read_files(self):
		for i in self.file_num_initials:
			f=open("./"+str(i)+self.file_affix,"r")
			data = f.readlines()
			last_row=data[-1].split(',')
			self.odom_error_pos.append(float(last_row[0].strip('"')))
			self.odom_error_rot.append(float(last_row[1].strip('"')))

	def plot(self):
		fig, ax1 = plt.subplots()
		ax2 = ax1.twinx()
		#fig=plt.figure()
		#ax=plt.axes()
		ax1.plot(self.file_num_initials,self.odom_error_pos,'b',label="Position Error(m)")
		ax2.plot(self.file_num_initials,self.odom_error_rot,'r',label="Rotation Error(degree)")
		ax1.legend( loc=2,fontsize = 'small', fancybox = True)
		ax2.legend( loc=1,fontsize = 'small', fancybox = True)
		plt.title("IMU Noise Multiplier vs Odometry Error")
		#plt.xlabel("Control Input Noise Standard Deviation")
		#plt.ylabel("Position Error ()")
		ax1.set_ylabel('Position Error (m)', color='b')
		ax2.set_ylabel('Rotation Error (degree)', color='r')
		ax1.set_xlabel('IMU Noise Multiplier')
		plt.savefig('imu_noise_vs_odometry_error_ateare.pdf')
		#plt.show()

class Plotter(object):
	def __init__(self):
		self.file_num_initials=[.1,.2,.4,.6,.8,1.0,1.2,1.4,1.6] #cut off at 1.6 , data available at 3.2, need .6,1.0,1.2,1.4
		self.odom_error_pos=[]
		self.odom_error_rot=[]
		self.file_affix='_noise_sigma_kitti.csv'
		self.plot_rot=False
		self.read_files()
		self.plot()
	def read_files(self):
		for i in self.file_num_initials:
			f=open("./input_noise/"+str(i)+self.file_affix,"r")
			data = f.readlines()
			last_row=data[-1].split(',')
			self.odom_error_pos.append(float(last_row[0].strip('"')))
			self.odom_error_rot.append(float(last_row[1].strip('"')))
			'''
			ate_acc=0
			are_acc=0
			for line in data:
				line_break=line.split(',')
				ate_acc+=float(line_break[0].strip('"'))
				are_acc+=float(line_break[1].strip('"'))
			ate_acc=ate_acc/len(data)
			are_acc=are_acc/len(data)
			self.odom_error_pos.append(ate_acc)
			self.odom_error_rot.append(are_acc)
			'''

	def plot(self):
		fig, ax1 = plt.subplots()

		if self.plot_rot==True:
			ax2 = ax1.twinx()
		#fig=plt.figure()
		#ax=plt.axes()
		ax1.plot(self.file_num_initials,self.odom_error_pos,'b',label="ATE")

		ax1.legend( loc=2,fontsize = 'small', fancybox = True)
		if self.plot_rot==True:
			ax2.plot(self.file_num_initials,self.odom_error_rot,'r',label="Rotation Error(degree)")
			ax2.legend( loc=1,fontsize = 'small', fancybox = True)
			ax2.set_ylabel('Rotation Error (degree)', color='r')
		plt.title("Control Input Noise Standard Deviation vs Odometry Error")
		#plt.xlabel("Control Input Noise Standard Deviation")
		#plt.ylabel("Position Error ()")
		ax1.set_ylabel('Average Translation Error (%)', color='b')
		ax1.set_xlabel('Input Noise Standard Deviation (degree)')
		plt.savefig('input_noise_sigma_vs_odometry_error_ateare.pdf')
		#plt.show()



class Plotter_Odometry_Comparison(object):
	def __init__(self):
		self.file_num_initials=[0] #cut off at 1.6 , data available at 3.2, need .6,1.0,1.2,1.4
		self.slam_position_record_x=[]
		self.gt_position_record_x=[]
		self.UC_slam_position_record_x=[]
		self.UC_gt_position_record_x=[]

		self.slam_position_record_y=[]
		self.gt_position_record_y=[]
		self.UC_slam_position_record_y=[]
		self.UC_gt_position_record_y=[]

		self.slam_position_record_z=[]
		self.gt_position_record_z=[]
		self.UC_slam_position_record_z=[]
		self.UC_gt_position_record_z=[]


		self.file_affix='_180_Naive.csv'
		self.read_files()
		#self.plot()
	def read_files(self):
		for i in self.file_num_initials:
			f=open("./Naive_FOV/"+str(i)+self.file_affix,"r")
			data = f.readlines()
			counter=0
			for line in data:
				counter+=1
				if counter==1:
					continue
				split_line=line.split(',')
				print("split_line",split_line)
				print("split_line_stripped",split_line[0].strip('"'))
				gt_x=float(split_line[0].strip('"'))
				gt_y=float(split_line[1].strip('"'))
				gt_z=float(split_line[2].strip('"'))
				slam_x=float(split_line[3].strip('"'))
				slam_y=float(split_line[4].strip('"'))
				slam_z=float(split_line[5].strip('"'))
				self.slam_position_record_x.append(slam_x)
				self.slam_position_record_y.append(slam_y)
				self.slam_position_record_z.append(slam_z)
				self.gt_position_record_x.append(gt_x)
				self.gt_position_record_y.append(gt_y)
				self.gt_position_record_z.append(gt_z)
			f=open("./Naive_FOV/UC/"+str(i)+self.file_affix,"r")
			data = f.readlines()
			counter=0
			for line in data:
				counter+=1
				if counter==1:
					continue
				split_line=line.split(',')
				gt_x=float(split_line[0].strip('"'))
				gt_y=float(split_line[1].strip('"'))
				gt_z=float(split_line[2].strip('"'))
				slam_x=float(split_line[3].strip('"'))
				slam_y=float(split_line[4].strip('"'))
				slam_z=float(split_line[5].strip('"'))
				self.UC_slam_position_record_x.append(slam_x)
				self.UC_slam_position_record_y.append(slam_y)
				self.UC_slam_position_record_z.append(slam_z)
				self.UC_gt_position_record_x.append(gt_x)
				self.UC_gt_position_record_y.append(gt_y)
				self.UC_gt_position_record_z.append(gt_z)
			self.plot(i)
			self.slam_position_record_x=[]
			self.slam_position_record_y=[]
			self.slam_position_record_z=[]
			self.gt_position_record_x=[]
			self.gt_position_record_y=[]
			self.gt_position_record_z=[]
			self.UC_slam_position_record_x=[]
			self.UC_slam_position_record_y=[]
			self.UC_slam_position_record_z=[]
			self.UC_gt_position_record_x=[]
			self.UC_gt_position_record_y=[]
			self.UC_gt_position_record_z=[]
	def plot(self,i):
		#fig, ax1 = plt.subplots()
		fig=plt.figure()
		ax1=plt.axes()
		#ax1= fig.gca(projection='3d')
		ax1.plot(self.gt_position_record_x,self.gt_position_record_y,'black',label="gt",linewidth=1)
		ax1.plot(self.slam_position_record_x,self.slam_position_record_y,'red',label="Ours",marker='o',linewidth=.5,linestyle="dashed",markersize=.5)
		ax1.plot(self.UC_slam_position_record_x,self.UC_slam_position_record_y,'blue',label="LIO-SAM",marker='o',linewidth=.5,linestyle="dashed",markersize=.5)
		#plt.title("Odometry, 180 FOV,sigma "+str(i)+" degrees")
		plt.title("Odometry, 180 FOV,naive policy, aim at mean center of all features")
		ax1.set_xlim(-20,70)
		ax1.set_ylim(-80,35)
		#plt.xlabel("Control Input Noise Standard Deviation")
		#plt.ylabel("Position Error ()")
		ax1.set_ylabel('m')
		ax1.set_xlabel('m')
		#ax1.set_zlabel('z (m)')
		ax1.legend( loc=2,fontsize = 'small', fancybox = True)
		plt.savefig(str(i)+'_naive_180FOV_odometry_comparison.pdf')
		#plt.show()


if __name__=='__main__':
	#pl=Plotter_C_UC()
	#pl=Plotter()
	#pl=Plotter_IMU()
	pl=Plotter_Odometry_Comparison()
