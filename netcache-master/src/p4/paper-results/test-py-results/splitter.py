import random
import math
import operator
file= open('zipf_sample_100000_05.txt','r')
train_file= open('train.txt','w')
test_file= open('test.txt','w')

lines= file.readlines()






# freq_dict= dict()
# current_read=0

# while current_read < len(lines):
# 	if lines[current_read] in freq_dict.keys():
# 		freq_dict[lines[current_read]] = freq_dict[lines[current_read]] + 1
# 	else:
# 		 freq_dict[lines[current_read]]= 1
# 	current_read = current_read + 1

# sorted_d = sorted(freq_dict.items(), key=operator.itemgetter(1),reverse=True)

# train_list=[]
# test_list=[]

# count=0

# for i in sorted_d:
# 	train_sample= int(math.floor(float(i[1])*0.7))
# 	test_sample= i[1] - train_sample
# 	if train_sample + test_sample != i[1]:
# 		print("NO", train_sample,test_sample,i[1]) 
# 	else:
# 		count= count + 1 
# 		# print("YES")
# 	for j in range(0,train_sample):
# 		train_list.append(i[0])
# 	for j in range(0,test_sample):
# 		test_list.append(i[0])

# random.shuffle(train_list)
# random.shuffle(test_list)

# for i in train_list:
# 	train_file.write(i)
# for i in test_list:
# 	test_file.write(i)

# print(len(sorted_d),count)
# print(len(train_list),len(test_list))






counter=0
random.shuffle(lines)
split= 0.7
split_index= int(math.floor(len(lines)*split))
training_lines= lines[:split_index]
testing_lines= lines[split_index:]

random.shuffle(training_lines)
random.shuffle(testing_lines)

for i in training_lines:
	train_file.write(i)

for i in range(0,10000):
	test_file.write(training_lines[i])
	
for i in testing_lines:
	test_file.write(i)