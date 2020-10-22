from map_class import map 
from route_class import route 
from route_class import nodes 

from Display import Display
import time

import os

temp = True
while temp:
    test =map("simpleTestMap.txt")
    test =map("testmap.txt")
    
    test2 = route(test)
    start_time = time.time()
    
    test2.BreathFirstSearch()
    test2.printRoute()
    print("--- %s sek ---" % ((time.time() - start_time)))

    #time.sleep(3)

    test3 = route(test)
    start_time = time.time()
    test3.A_star()
    test3.printRoute()
    print("--- %s sek ---" % ((time.time() - start_time)))
   
    dis = Display([12,7])
    first_node = nodes(None,test.pos_init,5,test.pos_cans,0)
    dis.runRoute(first_node,test2)

    temp =False

