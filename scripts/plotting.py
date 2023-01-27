import matplotlib.pyplot as plt
import numpy as np

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
		ax1.plot(self.file_num_initials,self.odom_error_pos,'r',label="Compensated ATE")
		if self.plot_rot==True:
			ax2.plot(self.file_num_initials,self.odom_error_rot,'b',label="Rotation Error")
			ax2.plot(self.file_num_initials,self.odom_error_rot_UC,'b-.',label="UC Rotation Error")
			ax2.legend( loc=1,fontsize = 'small', fancybox = True)
			ax2.set_ylabel('Yaw Erorr (degree/m)', color='b')
		ax1.plot(self.file_num_initials,self.odom_error_pos_UC,'r-.',label="Uncompensated ATE")


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



if __name__=='__main__':
	pl=Plotter_C_UC()
	pl=Plotter()
	pl=Plotter_IMU()

