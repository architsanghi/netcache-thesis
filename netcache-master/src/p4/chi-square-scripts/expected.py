# import argparse
# from subprocess import Popen
# from p4utils.utils.topology import Topology
# import time

# parser = argparse.ArgumentParser()
# parser.add_argument('--duration', nargs='?', type=int, default=40, help='Duration of traffic')


# args = parser.parse_args()
# duration= args.duration

# start_time= time.time()
# pid_list = []

# prev_list_normal=[]
# current_list_normal=[]

# prev_list=[]

# past_list= []

# iteration_number=0

# current_count=0


# prev_window= []

# f= open('normal.txt','w')
# # p1=(Popen("simple_switch_CLI --thrift-port 9090",shell=True))
# # pid_list.append(p1)
# # time.sleep(1)
# # pid_list.append(Popen("register_read ingress.my_reg 0",shell=True))
# # x= True
# while True:
# 	curr_window=[]
# 	time.sleep(3)
# 	p1=(Popen("simple_switch_CLI --thrift-port 9090 < commands1.txt >out1.txt",shell=True))
# 	p1.wait()

# 	p2=(Popen("simple_switch_CLI --thrift-port 9090 < commands2.txt >out2.txt",shell=True))
# 	p2.wait()

# 	myfile1=open("out1.txt","r")
# 	count1=0
# 	line1 = myfile1.readlines()
# 	# print(line)
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
# 	# print(line)
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


# 	if iteration_number==0:
# 		a=2
# 	else:
# 		#calculate current window distribution.

		
# 		for i in my_reg3:
# 			curr_window.append([i[0],i[1]])

# 		if prev_window==curr_window:
# 			print("Average computed")
# 			for item in curr_window:
# 				to_write1= str(item[0])
# 				to_write2= str(item[1]/iteration_number)
# 				f.write("%s," %to_write1)
# 				f.write("%s," %to_write2) 
# 			break


		
# 		for item in curr_window:
# 			to_write1= str(item[0])
# 			to_write2= str(item[1])
# 			f.write("%s," %to_write1)
# 			f.write("%s," %to_write2)



	
# 	f.write("\n")
# 	prev_list=my_reg3
# 	prev_window= curr_window
# 	iteration_number=iteration_number+1





# for pid in pid_list:
#     pid.wait()



import argparse
from subprocess import Popen
from p4utils.utils.topology import Topology
import time

parser = argparse.ArgumentParser()
parser.add_argument('--duration', nargs='?', type=int, default=40, help='Duration of traffic')


args = parser.parse_args()
duration= args.duration

start_time= time.time()
pid_list = []

prev_list_normal=[]
current_list_normal=[]

prev_list=[]

past_list= []

iteration_number=0

f= open('normal.txt','w')
file_probab= open('probab.txt','w')

probab_dict= dict()

total_dict= dict()

total_number_of_packets=0

while True:
	time.sleep(5)
	process_1=(Popen("simple_switch_CLI --thrift-port 9090 < commands1.txt >out1.txt",shell=True))
	process_1.wait()

	process_2=(Popen("simple_switch_CLI --thrift-port 9090 < commands2.txt >out2.txt",shell=True))
	process_2.wait()

	bl_code_file=open("out1.txt","r")
	bl_code_lines = bl_code_file.readlines()
	# print(line)
	bl_code_string= bl_code_lines[3]
	bl_code_string= bl_code_string[21:-1]
	bl_code_string= bl_code_string.split(", ")
	bl_code_array=[]
	for val in bl_code_string:
		bl_code_array.append(val)
	
	bl_code_file.close()


	bl_freq_file=open("out2.txt","r")
	bl_freq_lines = bl_freq_file.readlines()
	# print(line)
	bl_freq_string= bl_freq_lines[3]
	bl_freq_string= bl_freq_string[22:-1]
	bl_freq_string= bl_freq_string.split(", ")
	bl_freq_array=[]
	for val in bl_freq_string:
		bl_freq_array.append(val)
	
	bl_freq_file.close()

	for i in range(0,len(bl_code_array)):
		bl_code_array[i]= int(bl_code_array[i])

	for i in range(0,len(bl_freq_array)):
		bl_freq_array[i]=int(bl_freq_array[i])

	bl_code_freq=[]
	for i,j in zip(range(len(bl_code_array)),range(len(bl_freq_array))):
		bl_code_freq.append([bl_code_array[i],bl_freq_array[j]])

	total_packets=0

	if iteration_number!=0:

		curr_window=[]
		for i,j,k in zip(bl_code_freq,prev_list,past_list):
			temp_count= i[1]-j[1]
			total_packets= total_packets + temp_count
			current_count= temp_count
			curr_window.append([i[0],current_count])
			if i[0] in total_dict.keys():
				total_dict[i[0]]= total_dict[i[0]] + current_count
			else:
				total_dict[i[0]]= current_count

		if total_packets==0:
			sum_probability=0
			# print(len(probab_dict.keys()))
			# print(total_number_of_packets)
			
			# for i in probab_dict.keys():
			# 	probab_dict[i]= probab_dict[i]/iteration_number
			# 	print(i,"--->",probab_dict[i])
			# 	sum_probability= sum_probability + probab_dict[i] 
			# 	file_probab.write("%s " %str(i))
			# 	file_probab.write("%s " %str(probab_dict[i]))
			# 	file_probab.write("\n")
			
			for i in total_dict.keys():
				sum_probability= sum_probability + float(total_dict[i])/float(total_number_of_packets)
				print(i,"--->", float(total_dict[i])/float(total_number_of_packets))
				file_probab.write("%s " %str(i))
				file_probab.write("%s " %str(float(total_dict[i])/float(total_number_of_packets)))
				file_probab.write("\n")

			print("Sum of proabability is", sum_probability)
			print("end")
			break

		for item in curr_window:
			to_write1= str(item[0])
			to_write2= str(item[1])
			curr_probab= (float(item[1])/float(total_packets))
			if item[0] in probab_dict.keys():
				probab_dict[item[0]]= probab_dict[item[0]] + curr_probab
			else:
				probab_dict[item[0]]= curr_probab
			if(item[1]>0):
				print(item[0],"-->",item[1],"probability is",curr_probab)
			# f.write("%s," %to_write1)
			# f.write("%s," %to_write2)
			# f.write("\n")


	else:
		for i in bl_code_freq:
			to_write1= str(i[0])
			to_write2= str(i[1])
			# f.write("%s," %to_write1)
			# f.write("%s," %to_write2)
			total_packets= total_packets + i[1]
			if i[0] in total_dict.keys():
				total_dict[i[0]]= total_dict[i[0]]+ i[1]
			else:
				total_dict[i[0]]= i[1]

		for i in bl_code_freq:
			curr_probab= float(i[1])/float(total_packets)
			if i[1]>0:
				print(i[0],"-->",i[1],"probability is",curr_probab)
			if i[0] in probab_dict.keys():
				probab_dict[i[0]]= probab_dict[i[0]] + curr_probab
			else:
				probab_dict[i[0]]= curr_probab


	total_number_of_packets = total_number_of_packets + total_packets

	print("###########################")
	print("Total number of packets in a window",iteration_number,"are",total_packets)
	print("###########################")
	print("###########################")

	if total_packets==0:
		break

	# f.write("\n")
	prev_list=bl_code_freq
	if iteration_number==0:
		past_list= bl_code_freq
	else:
		past_list= curr_window
	iteration_number=iteration_number+1


for pid in pid_list:
    pid.wait()

