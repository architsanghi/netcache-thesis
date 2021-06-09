counter=0
file_reset_bl_code= open('test3.txt','w')
file_reset_bl_value= open('test4.txt','w')
for i in range(0,5):
	file_reset_bl_code.write("register_write bl_code " + str(counter) )
	file_reset_bl_code.write("\n")
	file_reset_bl_value.write("register_write bl_count " + str(counter) )
	file_reset_bl_value.write("\n")
	counter = counter + 1