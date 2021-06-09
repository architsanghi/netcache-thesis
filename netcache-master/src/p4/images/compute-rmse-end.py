import numpy as np
from sklearn.metrics import *
from math import *
import matplotlib.pyplot as plt

ground_truth_file= open("../../kv_store/attack-time-ground-truth.txt",'r')
predicted_file= open('file_attack_predicted.txt','r')




def mse(actual,pred):
	return mean_squared_error(actual,pred)

def rmse(actual_start,pred_start,actual_end,predicted_end):
	return sqrt(mean_squared_error(actual_end,predicted_end))

def mae(actual_start,pred_start,actual_end,predicted_end):
	return mean_absolute_error(actual_start,pred_start) + mean_absolute_error(actual_end,predicted_end)
	# return mean_absolute_error(actual_start,pred_start)
	#return mean_absolute_error(actual_end,predicted_end)

def l1_norm(actual_start,pred_start,actual_end,predicted_end):
	start_deviation= abs(actual_start - pred_start)
	end_deviation= abs(actual_end - predicted_end)
	l1_norm_deviation= (start_deviation + end_deviation)/2
	return l1_norm_deviation


def l2_norm(actual_start,pred_start,actual_end,predicted_end):
	start_deviation= pow(abs(actual_start - pred_start),2)
	end_deviation= pow(abs(actual_end - predicted_end),2)
	l2_norm_deviation= (start_deviation + end_deviation)/2
	return l2_norm_deviation







if __name__== "__main__":
	gt_line= ground_truth_file.readlines()
	pr_line= predicted_file.readlines()
	gt_start_array=[]
	gt_end_array=[]
	pr_start_array=[]
	pr_end_array=[]
	for line in gt_line:
		currline= line[0:]
		currline= currline.split(" ")
		gt_start_array.append(float(currline[0]))
		gt_end_array.append(float(currline[1]))
		
	for line in pr_line:
		currline= line[0:]
		currline= currline.split(" ")
		if currline!= "\n":
			pr_start_array.append(float(currline[0]))
			pr_end_array.append(float(currline[1]))

	# x_list= [4000,8000,12000,16000,20000]
	# y_list = []
	# y_list.append(rmse(gt_start_array[0:5],pr_start_array[0:5]))
	# y_list.append(rmse(gt_start_array[5:10],pr_start_array[5:10]))
	# y_list.append(rmse(gt_start_array[10:15],pr_start_array[10:15]))
	# y_list.append(rmse(gt_start_array[15:20],pr_start_array[15:20]))
	# y_list.append(rmse(gt_start_array[20:25],pr_start_array[20:25]))
	# print(x_list)
	# print(y_list)
	# plt.bar(x_list[0:], y_list[0:], color ='blue',width =500)
	# plt.xlabel("Number of Attack Queries")
	# plt.ylabel("RMSE Value for Attack Detection")
	# plt.title("RMSE VS Attack Queries")
	# plt.savefig("RMSE_Start.png")
	# plt.show()




	x_list= [10,20,30,40,50]
	y_list = []
	for i in range(0,5):
		y_list.append(rmse(gt_start_array[5*i:5*i + 5],pr_start_array[5*i:5*i + 5],gt_end_array[5*i:5*i + 5],pr_end_array[5*i:5*i + 5]))


	# y_list.append(rmse(gt_start_array[0:5],pr_start_array[0:5],gt_end_array[0:5],pr_end_array[0:5]))
	# y_list.append(rmse(gt_start_array[5:10],pr_start_array[5:10],gt_end_array[5:10],pr_end_array[5:10]))
	# y_list.append(rmse(gt_start_array[10:15],pr_start_array[10:15],gt_end_array[10:15],pr_end_array[10:15]))
	# y_list.append(rmse(gt_start_array[15:20],pr_start_array[15:20],gt_end_array[15:20],pr_end_array[15:20]))
	# y_list.append(rmse(gt_start_array[20:25],pr_start_array[20:25],gt_end_array[20:25],pr_end_array[20:25]))
	print(x_list)
	print(y_list)
	plt.bar(x_list[0:], y_list[0:], color ='blue',width =2)
	plt.xlabel("Percentage of Attack Queries")
	plt.ylabel("RMSE for Attack Detection")
	plt.title("RMSE VS Attack Queries")
	plt.savefig("RMSE_end.png")
	plt.show()

	



