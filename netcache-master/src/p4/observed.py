import argparse
from subprocess import Popen
from p4utils.utils.topology import Topology
import time
import matplotlib.pyplot as plt
import math
import scipy.stats

min_packet_threshold= 5 
chi_square_separator= 5

parser = argparse.ArgumentParser()
parser.add_argument('--duration', nargs='?', type=int, default=40, help='Duration of traffic')


args = parser.parse_args()
duration= args.duration

start_time= time.time()
pid_list = []

prev_list_normal=[]
current_list_normal=[]

iteration_number=0

f= open('attack.txt','w')

file_chisq= open('chi-sq-results.txt','w')

file_expected= open('probab.txt','r')

file_attack=open('./images/file_attack_predicted.txt',"a")

file_pos_weights= open('./images/positive-weights.txt',"a")

file_neg_weights= open('./images/negative-weights.txt',"a")

list_pos_weights=[]

list_neg_weights=[]

threshold_list= []

expected_lines= file_expected.readlines()

probab_dict= dict()

save_image_to= './images/'
file_count= open('./images/count.txt','r+')
count_lines= file_count.readlines()



for line in expected_lines:
	current_array= line.split(" ")
	if float(current_array[1]) > 0.0:
		probab_dict[int(current_array[0])]= float(current_array[1])

for key in probab_dict.keys():
	print(key,probab_dict[key])


def plot_graph(x, y, xlabel, ylabel, title,y1):
    plt.plot(x, y, 'r',marker='o',color='green')
    plt.plot(x,y1,'r',ls='--',color='red')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    file_last_line= count_lines[len(count_lines)-1]
    title_name= file_last_line[0:]
    next_file_number= int(title_name)
    next_file_number= next_file_number + 1
    file_count.write("\n")
    file_count.write(str(next_file_number))
    plt.savefig(save_image_to + str(title_name + '.png'))


def predict_attack_duration(chi_sq_list):
	start_flag=0
	end_flag= 0
	predicted_attack_start = 0
	predicted_attack_end= len(chi_sq_list) - 1
	for iterator in range(2,len(chi_sq_list)):
		if iterator > 0 and chi_sq_list[iterator-1] < chi_square_separator and chi_sq_list[iterator] > chi_square_separator and start_flag==0:
			predicted_attack_start= iterator
			start_flag=1
		if iterator > 0 and chi_sq_list[iterator] < chi_square_separator and chi_sq_list[iterator-1] > chi_square_separator and end_flag==0:
			predicted_attack_end= iterator
			end_flag=1 
	plt.axvline(x=predicted_attack_start,color='blue',ls=':')
	plt.axvline(x= predicted_attack_end,color='blue',ls=':')
	file_attack.write(str(predicted_attack_start*5 + 15))
	file_attack.write(" ")
	file_attack.write(str(predicted_attack_end*5 + 15))
	file_attack.write("\n")

def ground_truth_data():
	gt=open("../kv_store/attack-time-ground-truth.txt",'r')
	lines= gt.readlines()
	line_to_read= lines[len(lines)-1]
	required_array= line_to_read[0:-1]
	required_array= required_array.split(" ")
	gt_start= float(required_array[0])
	gt_end = float(required_array[1])
	gt_start= (gt_start - 15)/5
	gt_end= (gt_end - 15)/5

	
	plt.axvline(x= gt_start,color='orange',ls=':')
	plt.axvline(x=gt_end,color='orange',ls=':')

	
	



g=0
window_count= -1
chi_sq_list=[]

time.sleep(10)

while True:
	window_count= window_count + 1
	time.sleep(5)
	p1=(Popen("simple_switch_CLI --thrift-port 9090 < commands1.txt >out1.txt",shell=True))
	p1.wait()

	p2=(Popen("simple_switch_CLI --thrift-port 9090 < commands2.txt >out2.txt",shell=True))
	p2.wait()

	myfile1=open("out1.txt","r")
	count1=0
	line1 = myfile1.readlines()
	# print(line)
	line_to_read1= line1[3]
	required_array1= line_to_read1[21:-1]
	temp1= required_array1.split(", ")
	my_reg1=[]
	for val in temp1:
		my_reg1.append(val)
	
	myfile1.close()


	myfile2=open("out2.txt","r")
	count2=0
	line2 = myfile2.readlines()
	# print(line)
	line_to_read2= line2[3]
	required_array2= line_to_read2[22:-1]
	temp2= required_array2.split(", ")
	my_reg2=[]
	for val in temp2:
		my_reg2.append(val)
	
	myfile2.close()

	for i in range(0,len(my_reg1)):
		my_reg1[i]= int(my_reg1[i])

	for i in range(0,len(my_reg2)):
		my_reg2[i]=int(my_reg2[i])

	my_reg3=[]
	for i,j in zip(range(len(my_reg1)),range(len(my_reg2))):
		my_reg3.append([my_reg1[i],my_reg2[j]])


	# print(my_reg3)

	if iteration_number==0:
		packets_seen=0
		normal_list=[]
		for i in probab_dict.keys():
			normal_list.append(i)
		#calculate current window distribution.
		actual_bl_code={}
		actual_list=[]
		curr_window=[]
		for i in my_reg3:
			temp_count= i[1]
			current_count= temp_count
			packets_seen= packets_seen + temp_count
			curr_window.append([i[0],current_count])
			if current_count>0:
				actual_bl_code[i[0]]=current_count
				actual_list.append(i[0])
		
	else:
		packets_seen=0
		normal_list=[]
		# print(temp3)
		for i in probab_dict.keys():
			normal_list.append(i)
		#calculate current window distribution.
		actual_bl_code={}
		actual_list=[]
		curr_window=[]
		for i,j in zip(my_reg3,prev_list):
			temp_count= i[1]-j[1]
			current_count= temp_count
			packets_seen= packets_seen + temp_count
			curr_window.append([i[0],current_count])
			if current_count>0:
				actual_bl_code[i[0]]=current_count
				actual_list.append(i[0])


		
	if packets_seen==0:
		chi_sq_list= [math.log(x,2) for x in chi_sq_list]
		threshold_list= [math.log(x,2) for x in threshold_list]


		for i in list_pos_weights:
			file_pos_weights.write(str(i))
			file_pos_weights.write(" ")
		file_pos_weights.write("\n")
		for i in list_neg_weights:
			file_neg_weights.write(str(i))
			file_neg_weights.write(" ")
		file_neg_weights.write("\n")
		predict_attack_duration(chi_sq_list)
		ground_truth_data()
		plot_graph(range(0, len(chi_sq_list) ), chi_sq_list,'window number','log(chi sq deviation)','chi-sq deviation plot',threshold_list)
		# plot_graph(range(3, len(chi_sq_list) ), chi_sq_list[2:len(chi_sq_list)-1],'window number','log(chi sq deviation)','chi-sq deviation plot',threshold_list[2:len(chi_sq_list)-1])
		break
		#perform chi square with normal


	normal_only_list= [x for x in normal_list if x not in actual_list]
	actual_only_list= [x for x in actual_list if x not in normal_list]
	nrml_atck_int= set(normal_list).intersection(actual_list)
	print("intersection length is ",len(nrml_atck_int))

	# print("normaly only list is", len(normal_only_list),normal_only_list)

	print("actual only list is", actual_only_list)
	

	# print(normal_list)

	# print(actual_list)

	#chi square test
	chi_sq_normal=0

	for i in nrml_atck_int:
		observed_value= float(actual_bl_code[i])
		expected_value= (float(packets_seen)*probab_dict[i])
		expected_value= max(expected_value,min_packet_threshold)
		squared_val = (observed_value-expected_value)*(observed_value-expected_value)
		val_to_add= squared_val/expected_value
		print(i,observed_value,expected_value,probab_dict[i],val_to_add)
		chi_sq_normal= chi_sq_normal + val_to_add
		# if expected_value < min_packet_threshold and observed_value < min_packet_threshold:
		# 	e=0
		# else:
		# 	chi_sq_normal=chi_sq_normal+val_to_add

	for i in normal_only_list:
		observed_value= 0
		expected_value= (float(packets_seen)*probab_dict[i])
		if expected_value > 0:
			squared_val = (observed_value-expected_value)*(observed_value-expected_value)
			val_to_add= squared_val/expected_value
			print(i,observed_value,expected_value,probab_dict[i],val_to_add)
			
		chi_sq_normal= chi_sq_normal + val_to_add
		
		

	for i in actual_only_list:
		observed_value= actual_bl_code[i]
		expected_value= min_packet_threshold
		squared_val = (observed_value-expected_value)*(observed_value-expected_value)
		val_to_add= squared_val/expected_value
		print(i,observed_value,expected_value,probab_dict,val_to_add,"actual_only")
		chi_sq_normal=chi_sq_normal+val_to_add


	union_val= len(normal_list)+len(actual_list)-len(nrml_atck_int)
	if union_val>0:
		print("################ Normal chi square ################ ")
		print("Window: ",window_count)
		print(chi_sq_normal,union_val,packets_seen)
		curr_threshold= scipy.stats.chi2.ppf(0.99,union_val)
		threshold_list.append(curr_threshold)
		if chi_sq_normal - curr_threshold > 0:
			list_pos_weights.append(math.log(chi_sq_normal,2) - math.log(curr_threshold,2))
		else:
			list_neg_weights.append(math.log(chi_sq_normal,2) - math.log(curr_threshold,2))

	# printing_message= "Chi square results"
	# message_to_write= "Chi square results" + str(line_number) + "," str(chi_sq_normal) + "," + str(union_val)
	file_chisq.write("chi square results--> ")
	file_chisq.write("Current window is ")
	file_chisq.write(str(window_count))
	file_chisq.write(" ")
	file_chisq.write("Value for chi square is ")
	file_chisq.write(str(chi_sq_normal))
	chi_sq_list.append(chi_sq_normal)
	file_chisq.write(" ")
	file_chisq.write("Total number of equivalence classes ")
	file_chisq.write(str(union_val))
	file_chisq.write("\n")
	# f.write("%s,", message_to_write)
	

	
	for item in curr_window:
		to_write1= str(item[0])
		to_write2= str(item[1])
		f.write("%s," %to_write1)
		f.write("%s," %to_write2)



		#perform chi sqaure test ((o-e)^2)/e
		#write in a file the chi value.
	f.write("\n")
	prev_list=my_reg3
	iteration_number=iteration_number+1
	print("\n")

for pid in pid_list:
    pid.wait()






































# import argparse
# from subprocess import Popen
# from p4utils.utils.topology import Topology
# import time
# import matplotlib.pyplot as plt
# import math
# import scipy.stats

# min_packet_threshold= 8 

# start_time= time.time()
# pid_list = []

# iteration_number=0

# f= open('attack.txt','w')

# file_chisq= open('chi-sq-results.txt','w')

# file_expected= open('probab.txt','r')

# file_attack=open('./images/file_attack_predicted.txt',"a")

# file_pos_weights= open('./images/positive-weights.txt',"a")

# file_neg_weights= open('./images/negative-weights.txt',"a")

# zero_count= open('./zero_count.txt','w')

# list_pos_weights=[]

# list_neg_weights=[]

# threshold_list= []

# expected_lines= file_expected.readlines()

# probab_dict= dict()

# save_image_to= './images/'
# file_count= open('./images/count.txt','r+')
# count_lines= file_count.readlines()

# prev_freq_list={}
# prev_flag_list={}





# for line in expected_lines:
# 	current_array= line.split(" ")
# 	probab_dict[int(current_array[0])]= float(current_array[1])

# for key in probab_dict.keys():
# 	print(key,probab_dict[key])


# def plot_graph(x, y, xlabel, ylabel, title,y1):
#     plt.plot(x, y, 'r',marker='o',color='green')
#     plt.plot(x,y1,'r',ls='--',color='red')
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.title(title)
#     file_last_line= count_lines[len(count_lines)-1]
#     title_name= file_last_line[0:]
#     next_file_number= int(title_name)
#     next_file_number= next_file_number + 1
#     file_count.write("\n")
#     file_count.write(str(next_file_number))
#     plt.savefig(save_image_to + str(title_name + '.png'))


# def predict_attack_duration(chi_sq_list):
# 	start_flag=0
# 	end_flag= 0
# 	predicted_attack_start = 0
# 	predicted_attack_end= len(chi_sq_list) - 1
# 	for iterator in range(2,len(chi_sq_list)):
# 		if iterator > 0 and chi_sq_list[iterator-1] < 5 and chi_sq_list[iterator] > 5 and start_flag==0:
# 			predicted_attack_start= iterator
# 			start_flag=1
# 		if iterator > 0 and chi_sq_list[iterator] < 5 and chi_sq_list[iterator-1] > 5 and end_flag==0:
# 			predicted_attack_end= iterator
# 			end_flag=1 
# 	file_attack.write(str(predicted_attack_start*5 + 15))
# 	plt.axvline(x=predicted_attack_start,color='blue',ls=':')
# 	plt.axvline(x= predicted_attack_end,color='blue',ls=':')
# 	file_attack.write(" ")
# 	file_attack.write(str(predicted_attack_end*5 + 15))
# 	file_attack.write("\n")

# def ground_truth_data():
# 	gt=open("../kv_store/attack-time-ground-truth.txt",'r')
# 	lines= gt.readlines()
# 	line_to_read= lines[len(lines)-1]
# 	required_array= line_to_read[0:-1]
# 	required_array= required_array.split(" ")
# 	gt_start= float(required_array[0])
# 	gt_end = float(required_array[1])
# 	gt_start= (gt_start - 15)/5
# 	gt_end= (gt_end - 15)/5
# 	plt.axvline(x= gt_start,color='orange',ls=':')
# 	plt.axvline(x=gt_end,color='orange',ls=':')
# 	file_chisq.write(str(gt_start/5))
# 	file_chisq.write("\n")
# 	file_chisq.write(str(gt_end/5))

	
	


# g=0
# window_count= -1
# chi_sq_list=[]

# time.sleep(10)

# while True:
# 	window_count= window_count + 1
# 	time.sleep(5)
# 	p1=(Popen("simple_switch_CLI --thrift-port 9090 < commands1.txt >out1.txt",shell=True))
# 	p1.wait()

# 	p2=(Popen("simple_switch_CLI --thrift-port 9090 < commands2.txt >out2.txt",shell=True))
# 	p2.wait()

# 	myfile1=open("out1.txt","r")
# 	count1=0
# 	line1 = myfile1.readlines()
# 	line_to_read1= line1[3]
# 	required_array1= line_to_read1[21:-1]
# 	temp1= required_array1.split(", ")
# 	my_reg1=[]
# 	for val in temp1:
# 		my_reg1.append(val)
	
# 	myfile1.close()


# 	myfile2=open("out2.txt","r")
# 	count2=0
# 	line2 = myfile2.readlines()
# 	line_to_read2= line2[3]
# 	required_array2= line_to_read2[22:-1]
# 	temp2= required_array2.split(", ")
# 	my_reg2=[]
# 	for val in temp2:
# 		my_reg2.append(val)
	
# 	myfile2.close()

# 	for i in range(0,len(my_reg1)):
# 		my_reg1[i]= int(my_reg1[i])

# 	for i in range(0,len(my_reg2)):
# 		my_reg2[i]=int(my_reg2[i])

# 	my_reg3=[]
# 	for i,j in zip(range(len(my_reg1)),range(len(my_reg2))):
# 		my_reg3.append([my_reg1[i],my_reg2[j]])

# 	# print("######################")
# 	# print("######################")
# 	for i in prev_freq_list.keys():
# 		print(i,prev_freq_list[i],prev_flag_list[i])
# 	print("@@@@@@@@@@@@@@@@")
# 	if iteration_number==0:
# 		packets_seen=0
# 		normal_list=[]
# 		for i in probab_dict.keys():
# 			normal_list.append(i)
# 		#calculate current window distribution.
# 		actual_bl_code={}
# 		actual_list=[]
# 		curr_window=[]
# 		for i in my_reg3:
# 			temp_count= i[1]
# 			current_count= temp_count
# 			packets_seen= packets_seen + temp_count
# 			curr_window.append([i[0],current_count])
# 			if current_count>0:
# 				actual_bl_code[i[0]]=current_count
# 				actual_list.append(i[0])
# 				prev_freq_list[i[0]]= current_count
# 				prev_flag_list[i[0]]= 2
		
# 	else:
# 		packets_seen=0
# 		normal_list=[]
# 		for i in probab_dict.keys():
# 			normal_list.append(i)
# 		#calculate current window distribution.
# 		actual_bl_code={}
# 		actual_list=[]
# 		curr_window=[]
		
# 		for i in my_reg3:
# 			if i[0]!=0:
# 				print(i[0],i[1]) 
# 			if i[0] in prev_flag_list.keys() and prev_flag_list[i[0]]==2:
# 				temp_count= i[1]-prev_freq_list[i[0]]
# 				current_count= temp_count
# 				if temp_count < 0:
# 					print("something is wrong",i[0],i[1],prev_freq_list[i[0]]) 
# 				else:
# 					packets_seen= packets_seen + temp_count
# 				if current_count > 0:
# 					actual_bl_code[i[0]]=current_count
# 					actual_list.append(i[0])
# 					prev_freq_list[i[0]]= i[1]
# 					prev_flag_list[i[0]]= 2
# 					curr_window.append([i[0],current_count])
# 				elif current_count == 0 and i[0]!= 0:
# 					actual_bl_code[i[0]]=current_count
# 					actual_list.append(i[0])
# 					curr_window.append([i[0],current_count])
# 					# file_reset_bl_code= open('commands3.txt','w')
# 					file_reset_bl_value= open('commands4.txt','w')
# 					prev_flag_list[i[0]]= 1
# 					prev_freq_list[i[0]]=0
# 					# print("printing",prev_freq_list[i[0]])
# 					# file_reset_bl_code.write("register_write bl_code " + str(index_value) + str(" ") + "0")
# 					# file_reset_bl_code.write("\n")
# 					print("register_write bl_count " + str(i[0]) + str(" ") + "0")
# 					file_reset_bl_value.write("register_write bl_count " + str(i[0]) + str(" ") + "0")
# 					file_reset_bl_value.write("\n")
# 					# p3=(Popen("simple_switch_CLI --thrift-port 9090 < commands3.txt > out3.txt",shell=True))
# 					p4=(Popen("simple_switch_CLI --thrift-port 9090 < commands4.txt > out4.txt",shell=True))
# 					# p3.wait()
# 					p4.wait()
# 			elif i[0] not in prev_flag_list.keys() and i[0]!=0:
# 				print("this class is new",i[0])
# 				temp_count=i[1]
# 				current_count= temp_count
# 				actual_bl_code[i[0]]=current_count
# 				actual_list.append(i[0])
# 				prev_flag_list[i[0]]= 2
# 				prev_freq_list[i[0]]= i[1]
# 				packets_seen= packets_seen + temp_count
# 				curr_window.append([i[0],current_count])
# 			elif i[0] in prev_flag_list.keys() and prev_flag_list[i[0]]==1:
# 				temp_count=i[1]
# 				print("flag is 1", i[0],i[1],prev_freq_list[i[0]])
# 				current_count= temp_count
# 				actual_bl_code[i[0]]=current_count
# 				actual_list.append(i[0])
# 				if current_count > 0:
# 					prev_flag_list[i[0]]= 2
# 					prev_freq_list[i[0]]= i[1]
# 				elif current_count==0:
# 					prev_flag_list[i[0]]= 1
# 					prev_freq_list[i[0]]= 0
# 				packets_seen= packets_seen + temp_count
# 				curr_window.append([i[0],current_count])

			

# 		# for i in actual_bl_code:
# 		# 	print(i[0],i[1])
		
# 	if packets_seen==0:
# 		chi_sq_list= [math.log(x,2) for x in chi_sq_list]
# 		threshold_list= [math.log(x,2) for x in threshold_list]


# 		for i in list_pos_weights:
# 			file_pos_weights.write(str(i))
# 			file_pos_weights.write(" ")
# 		file_pos_weights.write("\n")
# 		for i in list_neg_weights:
# 			file_neg_weights.write(str(i))
# 			file_neg_weights.write(" ")
# 		file_neg_weights.write("\n")
# 		predict_attack_duration(chi_sq_list)
# 		ground_truth_data()
# 		# plot_graph(range(1, len(chi_sq_list) + 1), chi_sq_list,'window number','log(chi sq deviation)','chi-sq deviation plot',threshold_list)
# 		plot_graph(range(3, len(chi_sq_list) ), chi_sq_list[2:len(chi_sq_list)-1],'window number','log(chi sq deviation)','chi-sq deviation plot',threshold_list[2:len(chi_sq_list)-1])
# 		break
# 		#perform chi square with normal


# 	normal_only_list= [x for x in normal_list if x not in actual_list]
# 	actual_only_list= [x for x in actual_list if x not in normal_list]
# 	nrml_atck_int= set(normal_list).intersection(actual_list)
	
# 	# print("intersection lenght is ",len(nrml_atck_int))

# 	# print("normaly only list is", len(normal_only_list),normal_only_list)

# 	# print("actual only list is", actual_only_list)
	

# 	# print(normal_list)

# 	# print(actual_list)

# 	#chi square test
# 	chi_sq_normal=0

# 	for i in nrml_atck_int:
# 		observed_value= float(actual_bl_code[i])
# 		expected_value= (float(packets_seen)*probab_dict[i])
# 		squared_val = (observed_value-expected_value)*(observed_value-expected_value)
# 		val_to_add= squared_val/expected_value
# 		print(i,observed_value,expected_value,val_to_add)
# 		if expected_value < min_packet_threshold and observed_value < min_packet_threshold:
# 			chi_sq_normal = chi_sq_normal + 0
# 		else:
# 			chi_sq_normal=chi_sq_normal+val_to_add

# 	for i in normal_only_list:
# 		observed_value= 0
# 		expected_value= (float(packets_seen)*probab_dict[i])
# 		if expected_value > 0:
# 			squared_val = (observed_value-expected_value)*(observed_value-expected_value)
# 			val_to_add= squared_val/expected_value
# 			print(i,observed_value,expected_value,val_to_add)
			
# 		chi_sq_normal= chi_sq_normal + val_to_add
		
		

# 	for i in actual_only_list:
# 		observed_value= actual_bl_code[i]
# 		expected_value= 1
# 		squared_val = (observed_value-expected_value)*(observed_value-expected_value)
# 		val_to_add= squared_val/expected_value
# 		print(i,observed_value,expected_value,val_to_add)
# 		chi_sq_normal=chi_sq_normal+val_to_add


# 	union_val= len(normal_list)+len(actual_list)-len(nrml_atck_int)
# 	if union_val>0:
# 		print("################ Normal chi square ################ ")
# 		print("Window: ",window_count)
# 		print(chi_sq_normal,union_val,packets_seen)
# 		curr_threshold= scipy.stats.chi2.ppf(0.99,union_val)
# 		threshold_list.append(curr_threshold)
# 		if chi_sq_normal - curr_threshold > 0:
# 			list_pos_weights.append(math.log(chi_sq_normal,2) - math.log(curr_threshold,2))
# 		else:
# 			list_neg_weights.append(math.log(chi_sq_normal,2) - math.log(curr_threshold,2))

# 	# printing_message= "Chi square results"
# 	# message_to_write= "Chi square results" + str(line_number) + "," str(chi_sq_normal) + "," + str(union_val)
# 	file_chisq.write("chi square results--> ")
# 	file_chisq.write("Current window is ")
# 	file_chisq.write(str(window_count))
# 	file_chisq.write(" ")
# 	file_chisq.write("Value for chi square is ")
# 	file_chisq.write(str(chi_sq_normal))
# 	chi_sq_list.append(chi_sq_normal)
# 	file_chisq.write(" ")
# 	file_chisq.write("Total number of equivalence classes ")
# 	file_chisq.write(str(union_val))
# 	file_chisq.write("\n")
# 	# f.write("%s,", message_to_write)
	

	
# 	for item in curr_window:
# 		to_write1= str(item[0])
# 		to_write2= str(item[1])
# 		f.write("%s," %to_write1)
# 		f.write("%s," %to_write2)



# 		#perform chi sqaure test ((o-e)^2)/e
# 		#write in a file the chi value.
# 	f.write("\n")	
# 	iteration_number=iteration_number+1
# 	print("\n")

# for pid in pid_list:
#     pid.wait()

