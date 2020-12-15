from map_class import map 
from route_class import route 
from route_class import nodes 
from Display import Display
import psutil
import sys
import time
import os
import csv 

test =map(sys.argv[1])
print(sys.argv[1])
if (sys.argv[2] == "1"):
    
    print("-----------Running BFS-----------")
    test2 = route(test)
    start_time = time.time()
    data = test2.BreathFirstSearch()
    test2.printRoute()
    end_time = time.time()
    algo ="BFS"
    print("--- %s sek ---" % ((time.time() - start_time)))
    
else:
    print("-----------Running A* func 1-----------")
    test3 = route(test)
    start_time = time.time()
    data = test3.A_star(1)
    test3.printRoute()
    end_time = time.time()
    algo ="A*"
    print("--- %s sek ---" % ((time.time() - start_time)))

with open("Data/"+sys.argv[1]+"_"+algo+".csv", 'a') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow([sys.argv[3],end_time-start_time]+data) 

dis = Display([len(test.map[0]),len(test.map)])
first_node = nodes(None,test.pos_init,5,test.pos_cans,0)
dis.runRoute(first_node,test2)

