#!/bin/bash
#This is a comment

# my_dir= $(pwd)



p4dir=/home/p4/netcache/netcache-master/src/p4
cpdir=/home/p4/netcache/netcache-master/src/control_plane
kvdir=/home/p4/netcache/netcache-master/src/kv_store



echo $(pwd)

# cd $p4dir
# sudo p4run --config p4app_8_1.json

xterm -hold -e  "cd $p4dir; bash | sudo p4run --config p4app_8_1.json" &
PID1=$!

sleep 15

xterm -e "cd $cpdir; bash | sudo python controller.py" &
PID2=$!

sleep 3

xterm -e "cd $p4dir; bash | ./init_servers.sh 8" &
PID3=$!


xterm -e "cd $kvdir; bash | mkdir -p results | mx client1 python3 exec_queries.py --n-servers 8 --suppress --input data/dataset.txt" &
PID4=$!

sleep 3

xterm -e "cd $p4dir; bash | python observed.py" &
PID3=$!





# echo




wait $PID1
wait $PID2
wait $PID3
wait $PID4


