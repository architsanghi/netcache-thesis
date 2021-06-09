from client_api import NetCacheClient

import numpy as np
import time

# file_attack_info= open("/home/p4/Netcache-Chi-Sq/netcache-master/src/p4/images/attack-info.txt",'r')
# lines= file_attack_info.readlines()
# line_to_read= lines[len(lines)-1]
# required_array= line_to_read[0:-1]
# required_array= required_array.split(" ")
# attack_time= open("attack-time.txt",'a')
# start_query_number = int(float(required_array[0])*40000)
# end_query_number =  int(float(required_array[1])*40000)



def main(n_servers, disable_cache, suppress, input_files):
    client = NetCacheClient(n_servers=n_servers, no_cache=disable_cache)
    # current_query_number=0
    # start_time= time.clock()
    



    for filepath in input_files:
        sample = []

        with open(filepath) as fp:
            line = fp.readline()
            while line:
                sample.append(line.strip())
                line = fp.readline()

        # attack_time.write("going")
        # attack_time.write("\n")


        for query in sample:
            client.read(query, suppress=suppress)
            # if start_query_number == current_query_number:
            # 	time_elapsed= time.clock() - start_time
            # 	attack_time.write(str(time_elapsed))
            # 	attack_time.write(" ")
            # 	attack_time.write(str(start_query_number))
            # if end_query_number == current_query_number:
            # 	time_elapsed= time.clock() - start_time
            # 	attack_time.write(" ")
            # 	attack_time.write(str(time_elapsed))
            # 	attack_time.write("\n")
            # 	attack_time.write(str(end_query_number))
            # current_query_number= current_query_number + 1

          


        #print("\n########## SERVER METRICS REPORT ##########")
        #print("########## [{}] ##########\n".format(filepath))

        if disable_cache:
            x = 'nocache'
        else:
            x = 'netcache'

        input_file = filepath.split('/')[1].split('.')[0]

        out_file = 'results/{}_{}_{}.txt'.format(input_file, n_servers, x)
        out_fd = open(out_file, 'w')

        client.request_metrics_report(output=out_fd)


if __name__=="__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--n-servers', help='number of servers', type=int, required=False, default=1)
    parser.add_argument('--disable-cache', help='disable in-network caching', action='store_true')
    parser.add_argument('--suppress', help='suppress output', action='store_true')
    parser.add_argument('--input', help='input files to execute queries', required=True, nargs="+")
    args = parser.parse_args()

    main(args.n_servers, args.disable_cache, args.suppress, args.input)
