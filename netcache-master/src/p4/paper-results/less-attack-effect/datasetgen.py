total_legitimate_count = input ("Enter total number of legitimate items :")
total_attack_count= input("Enter total number of attack items: ")

total_items = total_legitimate_count + total_attack_count

data_set= open("dataset.txt","w")


read_file = open('test.txt', 'r')
zipf_Lines = read_file.readlines()

my_list=[]


attack_file=open('attack.txt','r')
attack_lines=attack_file.readlines()


zip_file_ptr=0
attack_file_ptr=0

current_items=0

# cache initialisation purpose
while current_items< 0.40*total_items:
	data_set.write(zipf_Lines[zip_file_ptr])
	zip_file_ptr= zip_file_ptr + 1
	current_items= current_items + 1
	total_legitimate_count= total_legitimate_count - 1
	if zipf_Lines[zip_file_ptr] not in my_list:
		my_list.append(zipf_Lines[zip_file_ptr])



while current_items < 0.60*total_items:
		data_set.write(attack_lines[attack_file_ptr])
		attack_file_ptr = attack_file_ptr + 1
		total_attack_count= total_attack_count - 1 
		current_items= current_items + 1


print(current_items,total_attack_count,total_legitimate_count)

while current_items< 0.75*total_items:
	data_set.write(zipf_Lines[zip_file_ptr])
	zip_file_ptr= zip_file_ptr + 1
	current_items= current_items + 1
	total_legitimate_count= total_legitimate_count - 1
	data_set.write(attack_lines[attack_file_ptr])
	attack_file_ptr = attack_file_ptr + 1
	total_attack_count= total_attack_count - 1 
	current_items= current_items + 1
	if zipf_Lines[zip_file_ptr] not in my_list:
		my_list.append(zipf_Lines[zip_file_ptr])


print(current_items,total_attack_count,total_legitimate_count)


# these zipf distribution should follow the expecnsive cpu path due to cache eviction.

while current_items < total_items and total_legitimate_count>0:
	data_set.write(zipf_Lines[zip_file_ptr])
	zip_file_ptr= zip_file_ptr + 1
	current_items= current_items + 1 
	total_legitimate_count= total_legitimate_count - 1
	if zip_file_ptr == len(zipf_Lines):
		break
	if zipf_Lines[zip_file_ptr] not in my_list:
		my_list.append(zipf_Lines[zip_file_ptr])
		


print("Number of distinct items are", len(my_list))
# print(my_list)
print(current_items,total_attack_count,total_legitimate_count)
