# #!/bin/bash
#This is a comment

# my_dir= $(pwd)



# p4dir=/home/p4/Desktop/netcache-thesis/netcache-master/src/p4
# cpdir=/home/p4/Desktop/netcache-thesis/netcache-master/src/control_plane
# kvdir=/home/p4/Desktop/netcache-thesis/netcache-master/src/kv_store
# memdir=/home/p4/Desktop/netcache-thesis/netcache-master/src/kv_store/data

p4dir="$(pwd)/src/p4"
cpdir="$(pwd)/src/control_plane"
kvdir="$(pwd)/src/kv_store"
memdir="$(pwd)/src/kv_store/data"


PID= echo "$$"


for((j=1;j<=1;j++));
do
	echo $j
	gnome-terminal -- bash -c "cd $p4dir; sudo p4run --config p4app_8_1.json;"&
	PID1=$!

	sleep 15

	gnome-terminal -- bash -c "cd $cpdir; sudo python controller.py;"&
	PID2=$!

	sleep 3

	gnome-terminal -- bash -c "cd $p4dir; ./init_servers.sh 8;bash"&
	PID3=$!

	sleep 3

	gnome-terminal -- bash -c "cd $memdir; python random-attack.py"&
	PID4=$!
	sleep 2


	gnome-terminal -- bash -c "cd $kvdir; mkdir -p results; mx client1 python3 exec_queries.py --n-servers 8 --suppress --input data/traffic.txt;"&
	PID5=$!

	sleep 1

	
	gnome-terminal -- bash -c "cd $p4dir; python observed.py; bash;"&
	PID6=$!

	sleep 180


	for i in ` ps -ef | grep -e 'p4run' | grep -v 'grep' | awk '{print $2}'`
	do 	
		echo $j
		# if [[ $i -ne $PID ]]
		# then
		# 	kill $i
		# fi
		sudo kill $i
	done

	for i in ` ps -ef | grep -e 'python' | grep -v 'grep' | awk '{print $2}'`
	do 	
		if [[ $i -ne $PID ]]
		then
			kill $i
		fi
		# sudo kill $i
	done

	for i in ` ps -ef | grep -e 'python3' | grep -v 'grep' | awk '{print $2}'`
	do 	
		# if [[ $i -ne $PID ]]
		# then
		# 	kill $i
		# fi
		sudo kill $i
	done

	for i in ` ps -ef | grep -e 'mx' | grep -v 'grep' | awk '{print $2}'`
	do 	
		if [[ $i -ne $PID ]]
		then
			kill $i
		fi
		# sudo kill $i
	done

	for i in ` ps -ef | grep -e 'kv_store' | grep -v 'grep' | awk '{print $2}'`
	do 	
		if [[ $i -ne $PID ]]
		then
			kill $i
		fi
		# sudo kill $i
	done

	for i in ` ps -ef | grep -e 'netcache' | grep -v 'grep' | awk '{print $2}'`
	do 	
		if [[ $i -ne $PID ]]
		then
			kill $i
		fi
		# sudo kill $i
	done


	




done




