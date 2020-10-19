from map_class import map 
from route_class import route 
from route_class import nodes 

from Display import Display
import time

import os

temp = True
while temp:
    test =map("simpleTestMap.txt")
    #test =map("testmap.txt")
    test.loadMap()
    print("here" )
    
    
    test2 = route(test)
    start_time = time.time()
    #test2.BreathFirstSearch()
    #test2.printRoute()
    print("--- %s sek ---" % ((time.time() - start_time)))

    #time.sleep(3)

    test =map("simpleTestMap.txt")
    test =map("testmap.txt")
    test.loadMap()
    test3 = route(test)
    start_time = time.time()
    test3.A_star()
    test3.printRoute()
    #test.printMap()
    print("--- %s sek ---" % ((time.time() - start_time)))
    

    test =map("simpleTestMap.txt")
    test =map("testmap.txt")
    test.loadMap()
    dis = Display([12,7])
    first_node = nodes(None,test,test.pos_init,5,test.pos_cans,0)
    dis.runRoute(first_node,test3)

    temp =False

