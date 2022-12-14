import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-whitegrid')

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
		fig=plt.figure()
		ax=plt.axes()
		one=ax.plot(self.file_num_initials,self.odom_error_pos,label="Position Erorr(m)")
		two=ax.plot(self.file_num_initials,self.odom_error_rotm,label="Yaw Erorr (degree)")
		legend = plt.legend(handles=[one, two], loc = 4, fontsize = 'small', fancybox = True)
		plt.title("IMU Noise vs Odometry Error")
		plt.show()



if __name__=='__main__':
	pl=Plotter()


