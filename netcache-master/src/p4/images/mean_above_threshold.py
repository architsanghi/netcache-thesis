import numpy as np
from sklearn.metrics import *
from math import *
import matplotlib.pyplot as plt

positive_file= open('positive-weights.txt','r')
negative_file= open('negative-weights.txt','r')

y_list_mean=[]
y_list_max= []

def mse(actual,pred,curr_batch):
	return mean_squared_error(actual,pred)

def rmse(actual,pred,curr_batch):
	return sqrt(mean_squared_error(actual,pred))

def mae(actual,pred,curr_batch):
	return mean_absolute_error(actual,pred)

def mean(curr_batch):
	batch_mean=[]
	for line in curr_batch:
		line_mean=[]
		line= line.split(" ")
		for i in line:
			if i!="\n":
				line_mean.append(float(i))
		mean_to_append= np.mean(line_mean)
		batch_mean.append(mean_to_append)

	final_batch_mean= np.mean(batch_mean)
	print(final_batch_mean)
	y_list_mean.append(final_batch_mean)

def find_max(curr_batch):
	batch_max=[]
	for line in curr_batch:
		line_max=[]
		line= line.split(" ")
		for i in line:
			if i!="\n":
				line_max.append(float(i))
		max_to_append= np.max(line_max)
		batch_max.append(max_to_append)

	final_batch_max= np.max(batch_max)
	y_list_max.append(final_batch_max)



if __name__== "__main__":
	pt_line= positive_file.readlines()
	nt_line= negative_file.readlines()

	mean(nt_line[0:1])

	for i in range(0,5):
		mean(pt_line[i*5:i*5 + 5])

	x_list= [0,10,20,30,40,50]
	plt.bar(x_list[0:1],y_list_mean[0:1],color='green',width=2)
	plt.bar(x_list[1:], y_list_mean[1:], color ='blue',width =2)
	plt.axhline(0,color='red')
	# plt.bar(x_list[0:],y_list_max[0:],color='red',width=500)
	plt.xlabel("Percentage of Attack Queries",fontsize=12)
	plt.ylabel("Mean Value Above Threshold",fontsize=12)
	plt.title("Mean Value Above Threshold VS % Attack Queries",fontsize=12)
	plt.savefig("Mean_Above_Threshold.png")
	plt.show()

	



	# x_list= [4000,8000,12000,16000,20000]
	# y_list = []
	# y_list.append(rmse(gt_end_array[0:5],pr_end_array[0:5]))
	# y_list.append(rmse(gt_end_array[5:10],pr_end_array[5:10]))
	# y_list.append(rmse(gt_end_array[10:15],pr_end_array[10:15]))
	# y_list.append(rmse(gt_end_array[15:20],pr_end_array[15:20]))
	# y_list.append(rmse(gt_end_array[20:25],pr_end_array[20:25]))
	# print(x_list)
	# print(y_list)
	# plt.bar(x_list[0:], y_list[0:], color ='blue',width =1000)
	# plt.xlabel("Number of Attack Queries")
	# plt.ylabel("RMSE Value for Attack Detection")
	# plt.title("RMSE VS Attack Queries")
	# plt.savefig("RMSE_End.png")
	# plt.show()

	



