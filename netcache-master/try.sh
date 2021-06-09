#!/bin/bash
# gnome-terminal -- bash -c "ls;"&


sleep 3

PID1= echo "$$"
# PID2= ps -ef | grep -e 'bash' | grep -v 'grep' | awk '{print $2}'

# echo $PID1

# for i in "${PID2[@]}"
# do 
	# killall -9 $i
	# if $i -ne PID1
	# 	then echo "$i"
	# else
	# 	echo "blabla"
# done

echo $PID1

# pkill --ns $503

for i in ` ps -ef | grep -e 'bash' | grep -v 'grep' | awk '{print $2}'`
do 	
	if [[ $i -ne $PID1 ]]
	then
		kill $i
	fi
done


# PID2= read -a arr <<< $ ps -ef | grep -e 'bash' | grep -v 'grep' | awk '{print $2}'


# myvar= \('abc' 'afjn' 'ajknf'\)
# echo $(myvar[@])


# echo $PID1
# echo $PID2

# PID3= $PID2 - $PID1

x1= ${PID2[@]/$PID1}
# echo $x1
echo $PID2

# kill $PID
























# #!/bin/bash
# #This is a comment

# # my_dir= $(pwd)



# p4dir=/home/p4/netcache/netcache-master/src/p4
# cpdir=/home/p4/netcache/netcache-master/src/control_plane
# kvdir=/home/p4/netcache/netcache-master/src/kv_store



# echo $(pwd)

# # cd $p4dir
# # sudo p4run --config p4app_8_1.json

# xterm -hold -e  "cd $p4dir; bash | sudo p4run --config p4app_8_1.json" &
# PID1=$! && echo SUCCESS || echo FAIL

# sleep 15

# xterm -e "cd $cpdir; bash | sudo python controller.py" &
# PID2=$! && echo SUCCESS || echo FAIL

# sleep 3

# xterm -e "cd $p4dir; bash | ./init_servers.sh 8" &
# PID3=$! && echo SUCCESS || echo FAIL


# xterm -e "cd $kvdir; bash | mkdir -p results | mx client1 python3 exec_queries.py --n-servers 8 --suppress --input data/dataset.txt" &
# PID4=$! && echo SUCCESS || echo FAIL

# sleep 3

# xterm -e "cd $p4dir; bash | python observed.py" &
# PID3=$! && echo SUCCESS || echo FAIL





# # echo




# wait $PID1
# wait $PID2
# wait $PID3
# wait $PID4





































# #!/bin/bash
#This is a comment

# my_dir= $(pwd)



########## WORKING CODE #################




p4dir=/home/p4/netcache-check-point-thesis-before-bash/netcache-master/src/p4
cpdir=/home/p4/netcache-check-point-thesis-before-bash/netcache-master/src/control_plane
kvdir=/home/p4/netcache-check-point-thesis-before-bash/netcache-master/src/kv_store
memdir=/home/p4/netcache-check-point-thesis-before-bash/netcache-master/src/kv_store/data
PID= echo "$$"

gnome-terminal -- bash -c "cd $p4dir; sudo p4run --config p4app_8_1.json;"&
PID1=$!

sleep 10

gnome-terminal -- bash -c "cd $cpdir; sudo python controller.py;"&
PID2=$!

sleep 3

gnome-terminal -- bash -c "cd $p4dir; ./init_servers.sh 8;bash"&
PID3=$! && echo SUCCESS || echo FAIL


sleep 3
gnome-terminal -- bash -c "cd $kvdir; mkdir -p results; mx client1 python3 exec_queries.py --n-servers 8 --suppress --input data/test.txt;"&
PID4=$! && echo SUCCESS || echo FAIL


sleep 3 
gnome-terminal -- bash -c "cd $p4dir; python observed.py; bash;"&
PID5=$! && echo SUCCESS || echo FAIL


sleep 50

# for i in ` ps -ef | grep -e 'bash' | grep -v 'grep' | awk '{print $2}'`
# do 	
# 	# if [[ $i -ne $PID ]]
# 	# then
# 	# 	kill $i
# 	# fi
# 	sudo kill $i
# done


for i in ` ps -ef | grep -e 'python' | grep -v 'grep' | awk '{print $2}'`
do 	
	# if [[ $i -ne $PID ]]
	# then
	# 	kill $i
	# fi
	sudo kill $i
done

for i in ` ps -ef | grep -e 'p4run' | grep -v 'grep' | awk '{print $2}'`
do 	
	# if [[ $i -ne $PID ]]
	# then
	# 	kill $i
	# fi
	sudo kill $i
done


for i in ` ps -ef | grep -e 'mx' | grep -v 'grep' | awk '{print $2}'`
do 	
	# if [[ $i -ne $PID ]]
	# then
	# 	kill $i
	# fi
	sudo kill $i
done

for i in ` ps -ef | grep -e 'netcache' | grep -v 'grep' | awk '{print $2}'`
do 	
	# if [[ $i -ne $PID ]]
	# then
	# 	kill $i
	# fi
	sudo kill $i
done


