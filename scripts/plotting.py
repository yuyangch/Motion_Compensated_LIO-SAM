import matplotlib.pyplot as plt
import numpy as np

#plt.style.use('seaborn-whitegrid')

class Plotter(object):
	def __init__(self):
		self.file_num_initials=[1,2,4,8,16,18,20,24,32]
		self.odom_error_pos=[]
		self.odom_error_rot=[]
		self.file_affix='x_imu.csv'
		self.read_files()
		self.plot()
	def read_files(self):
		for i in self.file_num_initials:
			f=open(str(i)+self.file_affix,"r")
			data = f.readlines()
			last_row=data[-1].split(',')
			self.odom_error_pos.append(float(last_row[0].strip('"')))
			self.odom_error_rot.append(float(last_row[1].strip('"')))

	def plot(self):
		fig, ax1 = plt.subplots()

		ax2 = ax1.twinx()
		#fig=plt.figure()
		#ax=plt.axes()
		ax1.plot(self.file_num_initials,self.odom_error_pos,'b',label="Position Erorr(m)")
		ax2.plot(self.file_num_initials,self.odom_error_rot,'r',label="Yaw Erorr (degree)")
		ax1.legend( loc=2,fontsize = 'small', fancybox = True)
		ax2.legend( loc=1,fontsize = 'small', fancybox = True)
		plt.title("IMU Noise vs Odometry Error")
		plt.xlabel("IMU Noise Factor")
		#plt.ylabel("Position Error ()")
		ax1.set_ylabel('Position Error (m)', color='b')
		ax2.set_ylabel('Yaw Erorr (degree)', color='r')
		plt.savefig('imu_noise_vs_odometry_error.pdf')
		#plt.show()



if __name__=='__main__':
	pl=Plotter()


