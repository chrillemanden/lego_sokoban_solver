from map_class import map 
from heapq import heappush, heappop
import numpy as np
import copy
import math
import time


number_of_nodes = 0


class nodes:
    def __init__(self,parent_node,current_map,pos,last_move,cans,depth):
        self.next_nodes = []
        self.parent_node = parent_node
        self.legal = 1
        self.current_map = current_map
        self.current_postion = pos
        self.current_pos_cans = cans
        self.last_move = last_move
        self.with_can = 0
        self.score = 0
        self.depth = depth

    
    def setNextNodes(self,nodes):
        self.next_nodes = nodes


class route:
    def __init__(self, map):
        self.map = map
        self.optimal_route = []
        self.possible_steps = []
        self.possible_steps.append([1,0]) #DOWN
        self.possible_steps.append([-1,0]) #UP
        self.possible_steps.append([0,1]) #RIGHT
        self.possible_steps.append([0,-1]) #LEFT
        self.maps_tried = [self.map.map]
        self.maps_tried2 = [[None]]*(len(self.map.map)*len(self.map.map[0]))
        self.dictionary = {'Start': 1}
        self.open_list = []
        self.route = []

    def printRoute(self):
        f = open("Route.txt", "w")
        for i in range(len(self.route)):
            f.write(self.route[i])
        f.close()

    def checkIfDone(self,current_pos_cans):
        number_of_cans_at_goal = 0

        for pos in self.map.pos_goal:
            for cans in current_pos_cans:
                if pos == cans:
                    #print( pos )
                    #print (cans)
                    number_of_cans_at_goal = number_of_cans_at_goal + 1
        
        if number_of_cans_at_goal == len(self.map.pos_goal):
            return 1
        else:
            return 0

    def legalMove(self,move,node): # ONLY checks if the move is legal
                                    # return 0 if not legal
                                    # return 1 if legal
                                    # return 2 if leagl and moves a can
        new_pos = [node.current_postion[0]+self.possible_steps[move][0], node.current_postion[1]+self.possible_steps[move][1]]
        if(node.current_map.map[new_pos[0]][new_pos[1]]=='.'):
            return 1
        elif(node.current_map.map[new_pos[0]][new_pos[1]] == 'X'):
            return 0
        elif(node.current_map.map[new_pos[0]][new_pos[1]] == 'J'):
            new_pos_can = [new_pos[0]+self.possible_steps[move][0], new_pos[1]+self.possible_steps[move][1]]
            if(node.current_map.map[new_pos_can[0]][new_pos_can[1]] == 'J'):
                return 0
            elif(node.current_map.map[new_pos_can[0]][new_pos_can[1]] == 'X'):
                return 0
            elif(node.current_map.map[new_pos_can[0]][new_pos_can[1]] == '.'):
                for test_move in range(len(self.possible_steps)):
                    new_pos_can_temp = [new_pos_can[0]+self.possible_steps[test_move][0], new_pos_can[1]+self.possible_steps[test_move][1]]
                    #print("Deadlock FOUND")
                    if(node.current_map.map[new_pos_can_temp[0]][new_pos_can_temp[1]] == 'X'):
                        new_pos_can_down = [new_pos_can[0]+self.possible_steps[0][0], new_pos_can[1]+self.possible_steps[0][1]]
                        new_pos_can_up = [new_pos_can[0]+self.possible_steps[1][0], new_pos_can[1]+self.possible_steps[1][1]]
                        new_pos_can_right = [new_pos_can[0]+self.possible_steps[2][0], new_pos_can[1]+self.possible_steps[2][1]]
                        new_pos_can_left = [new_pos_can[0]+self.possible_steps[3][0], new_pos_can[1]+self.possible_steps[3][1]]
                        if((test_move == 0  or test_move == 1) and  (node.current_map.map[new_pos_can_left[0]][new_pos_can_left[1]] == 'X' or node.current_map.map[new_pos_can_right[0]][new_pos_can_right[1]] == 'X') ):
                            #print("Deadlock FOUND")
                            return 0
                        elif((test_move == 2  or test_move == 3) and  (node.current_map.map[new_pos_can_up[0]][new_pos_can_up[1]] == 'X' or node.current_map.map[new_pos_can_down[0]][new_pos_can_down[1]] == 'X') ):
                            #print("Deadlock FOUND")
                            return 0
                return 2
            elif(self.map.map[new_pos_can[0]][new_pos_can[1]] == 'G'):
                return 2

        elif(self.map.map[new_pos[0]][new_pos[1]] == 'G'):
            return 1

        return 0
        
        

    def updateMap(self,move,node,with_can): # update the map
        new_pos = [node.current_postion[0]+self.possible_steps[move][0], node.current_postion[1]+self.possible_steps[move][1]]
        for i in range(len(self.map.pos_goal)):
            node.current_map.map[self.map.pos_goal[i][0]][self.map.pos_goal[i][1]] = 'G' 
        node.current_map.map[node.current_postion[0]][node.current_postion[1]] = '.'
        node.current_map.map[new_pos[0]][new_pos[1]] = 'M'  

        if (with_can == 1):
            new_pos_can = [new_pos[0]+self.possible_steps[move][0], new_pos[1]+self.possible_steps[move][1]]
            for pos_cans in range(len(node.current_pos_cans)):
                if node.current_pos_cans[pos_cans] == new_pos:
                    node.current_pos_cans[pos_cans] = new_pos_can
                    node.current_map.map[node.current_pos_cans[pos_cans][0]][node.current_pos_cans[pos_cans][1]] = 'J'
        node.current_postion = new_pos
        for i in range(len(node.current_pos_cans)):
            node.current_map.map[node.current_pos_cans[i][0]][node.current_pos_cans[i][1]] = 'J'         


    def addMove(self,move,with_can):
        if with_can == 0:
            if move == 0:
                self.route.insert(0,"d")
            elif move == 1:
                self.route.insert(0,"u")
            elif move == 2:
                self.route.insert(0,"r")
            elif move == 3:
                self.route.insert(0,"l")
        else:
            if move == 0:
                self.route.insert(0,"D")
            elif move == 1:
                self.route.insert(0,"U")
            elif move == 2:
                self.route.insert(0,"R")
            elif move == 3:
                self.route.insert(0,"L")

    def checkIftried(self,node):
        temp_map = node.current_map.map
        #print(len(self.maps_tried))
        for i in range(len(self.maps_tried)):
            if temp_map == self.maps_tried[i]:
                node.legal = 0
                return
        self.maps_tried.append(node.current_map.map)

    def checkIftried2(self,node):
        temp_map = node.current_map.map
        temp_current_pos = node.current_postion

        index = temp_current_pos[1]*len(self.map.map)+temp_current_pos[0]
        if len(self.maps_tried2[index]) == 1:
            self.maps_tried2[index] = self.maps_tried2[index]+ [node.current_map.map]
            return

        for i in range(len(self.maps_tried2[index])):
            if temp_map == self.maps_tried2[index][i]:
                # print(temp_map == self.maps_tried2[index][i])
                # print(temp_map)
                # print("ww")
                # print(self.maps_tried2[index][i])
                node.legal = 0
                return
        self.maps_tried2[index] = self.maps_tried2[index]+ [node.current_map.map]
        #print(self.maps_tried2[index])
        #while(1):
        #    index = 0

    def checkIftried3(self,node):
        temp_current_pos = node.current_postion
        index = str(temp_current_pos[0])
        index += str(temp_current_pos[1])
        number_added = 0
        sorted_pos = sorted(node.current_pos_cans)
        for i in range(len(sorted_pos)):
            index += str(sorted_pos[i][0])
            index += str(sorted_pos[i][1])

        if not(index in self.dictionary):
            self.dictionary[index] = 1
        else:
            node.legal = 0
    
    def findroute(self,node): 
        
        if node.last_move != 5 and node.parent_node != None:
            self.addMove(node.last_move,node.with_can)
            node.last_move = 5
            self.findroute(node.parent_node)
        

                    

    def BreathFirstSearch(self):
        first_node = nodes(None,self.map,self.map.pos_init,5,self.map.pos_cans,0)
        
        global number_of_nodes
        number_of_nodes = 0
        result = 0
        i = 1
        current_depth = 0
        self.open_list.append(first_node)
        while(len(self.open_list) >0 and result != 1):
            node = self.open_list.pop(0)
            number_of_maps_tried = 0
            #for i in range(len(self.maps_tried2)):
            #    number_of_maps_tried += len(self.maps_tried2[i])
                
            #print( "Current depth: " +str(current_depth)+ " Number of Nodes: " + str(number_of_nodes)+ " Elements in maps_tried: " + str(len(self.dictionary))+ " Elements in open_list: " + str(len(self.open_list)))
            result = 0
            if(node.legal == 1):
                if current_depth < node.depth:
                    current_depth = node.depth 
                for move in range(len(self.possible_steps)):

                    if ( len(node.next_nodes) != 4):
                        node.next_nodes.append(nodes(node,copy.deepcopy(node.current_map),copy.deepcopy(node.current_postion),move,copy.deepcopy(node.current_pos_cans),node.depth+1))
                        
                        number_of_nodes = number_of_nodes + 1
                        is_legal = self.legalMove(move,node.next_nodes[move])
                        if(is_legal == 1):
                            self.updateMap(move,node.next_nodes[move],0)
                            self.checkIftried3(node.next_nodes[move])
                        elif(is_legal == 2):
                            self.updateMap(move,node.next_nodes[move],1)
                            self.checkIftried3(node.next_nodes[move])
                            node.next_nodes[move].with_can = 1
                        else:
                            node.next_nodes[move].legal = 0
                        
                        if(node.next_nodes[move].legal == 1):
                            self.open_list.append(node.next_nodes[move])

                        if (self.checkIfDone(node.next_nodes[move].current_pos_cans) == 1):
                            print(node.depth)
                            self.addMove(move,node.next_nodes[move].with_can)

                            self.map.map = node.next_nodes[move].current_map.map
                            self.findroute(node)
                            result = 1
        print( "Current depth: " +str(current_depth)+ " Number of Nodes: " + str(number_of_nodes)+ " Elements in maps_tried: " + str(len(self.dictionary))+ " Elements in open_list: " + str(len(self.open_list)))
        print(self.route)
        #self.map.printMap()

    def find_score(self,node):

        score =  node.depth
        
        for pos_cans in node.current_pos_cans:
            shortest_dis = 100000
            dist = math.sqrt((pos_cans[0]-node.current_postion[0])**2+(pos_cans[1]-node.current_postion[1])**2)
            #dist = abs(pos_cans[0]-goal_pos[0])+abs(pos_cans[1]-goal_pos[1])
            if dist < shortest_dis :
                shortest_dis = dist
        score +=shortest_dis

        for pos_cans in node.current_pos_cans:
            shortest_dis = 100000
            for goal_pos in self.map.pos_goal:
                dist = math.sqrt((pos_cans[0]-goal_pos[0])**2+(pos_cans[1]-goal_pos[1])**2)
                #dist = abs(pos_cans[0]-goal_pos[0])+abs(pos_cans[1]-goal_pos[1])
                if dist < shortest_dis :
                    shortest_dis = dist
                    if(pos_cans == goal_pos):
                        score += -1
            score +=shortest_dis
        node.score = score

    def find_score2(self,node):

        score = node.depth
        
        for pos_cans in node.current_pos_cans:
            shortest_dis = 100000
            dist = math.sqrt((pos_cans[0]-node.current_postion[0])**2+(pos_cans[1]-node.current_postion[1])**2)
            #dist = abs(pos_cans[0]-goal_pos[0])+abs(pos_cans[1]-goal_pos[1])
            if dist < shortest_dis :
                shortest_dis = dist
        score +=shortest_dis
        
        for pos_cans in node.current_pos_cans:
            shortest_dis = 100000
            for goal_pos in self.map.pos_goal:
                dist = math.sqrt((pos_cans[0]-goal_pos[0])**2+(pos_cans[1]-goal_pos[1])**2)
                #dist = abs(pos_cans[0]-goal_pos[0])+abs(pos_cans[1]-goal_pos[1])
                if dist < shortest_dis :
                    shortest_dis = dist
                    if(pos_cans == goal_pos):
                        score += -1
            score +=shortest_dis
        
        if (node.last_move == node.parent_node.last_move):
            score += -2
        else:
            if (node.last_move == 0) and (node.parent_node.last_move == 2 or node.parent_node.last_move == 3):
               score += 1
            elif(node.last_move == 1) and (node.parent_node.last_move == 2 or node.parent_node.last_move == 3):
               score += 1
            elif(node.last_move == 2) and (node.parent_node.last_move == 0 or node.parent_node.last_move == 1):
                score += 1
            elif(node.last_move == 3) and (node.parent_node.last_move == 0 or node.parent_node.last_move == 1):
                score += 1
            elif(node.last_move == 0 and node.parent_node == 1):
                score += 3
            elif(node.last_move == 1 and node.parent_node == 0):
                score += 3
            elif(node.last_move == 2 and node.parent_node == 3):
                score += 3
            elif(node.last_move == 3 and node.parent_node == 2):
                score += 3
        node.score = score

    def binarySearch(self,node, low, high): 

        if low == high: 
            if self.open_list[low].score > node.score: 
                return low 
            else: 
                return low+1
        if low > high: 
            return low 
    
        mid = (low+high)//2
        if self.open_list[mid].score < node.score: 
            return self.binarySearch(node, mid+1, high) 
        elif self.open_list[mid].score > node.score: 
            return self.binarySearch(node, low, mid-1) 
        else: 
            return mid 

    def listsearch(self,node):
        if(len(self.open_list) == 0):
            return 0
        
        for i in range(len(self.open_list)):
            if self.open_list[i].score >= node.score :
                return i
        return len(self.open_list)



    def A_star(self):

        first_node = nodes(None,self.map,self.map.pos_init,5,self.map.pos_cans,0)
        
        global number_of_nodes
        number_of_nodes = 0
        result = 0
        i = 1
        current_depth = 0
        #self.open_list.append(first_node)
        heappush(self.open_list,(1.,id(first_node),first_node))
        while(len(self.open_list) >0 and result != 1 ):
            node = heappop(self.open_list)[2]#self.open_list.pop(0)
            #node = self.open_list.pop(0)
            print("Current depth: " +str(current_depth)+ " Number of Nodes: " + str(number_of_nodes)+ " Elements in maps_tried: " + str(len(self.dictionary))+ " Elements in open_list: " + str(len(self.open_list))+" Current score: " +str(node.score))
            result = 0
            if(node.legal == 1):
                current_depth = node.depth 
                for move in range(len(self.possible_steps)):

                    if ( len(node.next_nodes) != 4):
                        node.next_nodes.append(nodes(node,copy.deepcopy(node.current_map),copy.deepcopy(node.current_postion),move,copy.deepcopy(node.current_pos_cans),node.depth+1))
                        number_of_nodes = number_of_nodes + 1
                        is_legal = self.legalMove(move,node.next_nodes[move])

                        if(is_legal == 1):
                            self.updateMap(move,node.next_nodes[move],0)
                            self.checkIftried3(node.next_nodes[move])
                        elif(is_legal == 2):
                            self.updateMap(move,node.next_nodes[move],1)
                            self.checkIftried3(node.next_nodes[move])
                            node.next_nodes[move].with_can = 1
                        else:
                            node.next_nodes[move].legal = 0
                        if node.next_nodes[move].legal == 1:
                            #self.open_list.insert(self.listsearch(node.next_nodes[move]),node.next_nodes[move])
                            self.find_score2(node.next_nodes[move])
                            #self.open_list.insert(self.binarySearch(node.next_nodes[move],0,len(self.open_list)-1),node.next_nodes[move])
                            heappush(self.open_list,(node.next_nodes[move].score,id(node.next_nodes[move]) , node.next_nodes[move]))
                        
                        if (self.checkIfDone(node.next_nodes[move].current_pos_cans) == 1):
                            print(node.depth)
                            self.addMove(move,node.next_nodes[move].with_can)
                            self.map.map = node.next_nodes[move].current_map.map
                            self.findroute(node)
                            result = 1
        
        
                
        print("Current depth: " +str(current_depth)+" Current score: " +str(node.score)+ " Number of Nodes: " + str(number_of_nodes)+ " Elements in maps_tried: " + str(len(self.dictionary))+ " Elements in open_list: " + str(len(self.open_list)))
        print(self.route)
