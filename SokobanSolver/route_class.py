from map_class import map 
from heapq import heappush, heappop
import numpy as np
import copy
import math
import time
from functools import reduce
import operator



number_of_nodes = 0


class nodes:
    def __init__(self,parent_node,pos,last_move,cans,depth):
        self.next_nodes = []
        self.parent_node = parent_node
        self.legal = 1
#        self.current_map = current_map
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
        self.dictionary = {'Start': 1}
        self.open_list = []
        self.route = []

    def printRoute(self):
        f = open("Route.txt", "w")
        for i in range(len(self.route)):
            f.write(self.route[i])
        f.close()

    def checkIfDone(self,current_pos_cans):
        #number_of_cans_at_goal = 0


        if (all(elem in self.map.pos_goal  for elem in current_pos_cans)):
            return 1
        else:
            return 0

    def legalMove(self,move,node): # ONLY checks if the move is legal
                                    # return 0 if not legal
                                    # return 1 if legal
                                    # return 2 if leagl and moves a can
        new_pos = [node.current_postion[0]+self.possible_steps[move][0], node.current_postion[1]+self.possible_steps[move][1]]
        index = str(new_pos[0])+","+str(new_pos[1])
        if(new_pos in node.current_pos_cans):
            new_pos_can = [new_pos[0]+self.possible_steps[move][0], new_pos[1]+self.possible_steps[move][1]]
            index_can = str(new_pos_can[0])+","+str(new_pos_can[1])
            if(new_pos_can in node.current_pos_cans):
                return 0
            elif(self.map.map_dictonary[index_can] == 1):
                return 2
            elif(self.map.map_dictonary[index_can] == 0):
                return 0
            elif(self.map.map_dictonary[index_can] == 2 ):
                return 0
        elif(self.map.map_dictonary[index]== 0):
            return 0
        elif(self.map.map_dictonary[index]== 1):
            return 1
        elif(self.map.map_dictonary[index]== 2):
            return 1
        return 3
        

    def updateMap(self,move,node,with_can): # update the map
        new_pos = [node.current_postion[0]+self.possible_steps[move][0], node.current_postion[1]+self.possible_steps[move][1]]
        if (with_can == 1):
            new_pos_can = [new_pos[0]+self.possible_steps[move][0], new_pos[1]+self.possible_steps[move][1]]
            index = (node.current_pos_cans.index(new_pos))
            node.current_pos_cans[index] = new_pos_can
        node.current_postion = new_pos

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
        sorted_pos = (sorted(node.current_pos_cans))
        index = str(node.current_postion).join(str(reduce(lambda x,y: x+y,sorted_pos)))
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
        first_node = nodes(None,self.map.pos_init,5,self.map.pos_cans,0)
        node_temp_current_pos = [0,0]
        node_temp_cans_pos = [0,0]
        global number_of_nodes
        number_of_nodes = 0
        result = 0
        current_depth = 0
        self.open_list.append(first_node)
        while(len(self.open_list) >0 and result != 1):
            node = self.open_list.pop(0)
            number_of_maps_tried = 0
            if(node.legal == 1):                
                node_temp_current_pos = list(node.current_postion)
                #print("Current depth: " +str(current_depth)+ " Number of Nodes: " + str(number_of_nodes)+ " Elements in maps_tried: " + str(len(self.dictionary))+ " Elements in open_list: " + str(len(self.open_list))+" Current score: " +str(node.score))
                for move in range(len(self.possible_steps)):
                    node_temp_cans_pos = list(node.current_pos_cans)
                    node.next_nodes.append(nodes(node,node_temp_current_pos,move,node_temp_cans_pos,node.depth+1))
                    number_of_nodes = number_of_nodes + 1
                    is_legal = self.legalMove(move,node.next_nodes[move])
                    if(is_legal > 0):
                        self.updateMap(move,node.next_nodes[move],is_legal-1)
                        self.checkIftried(node.next_nodes[move])
                        node.next_nodes[move].with_can = is_legal-1
                        if(node.next_nodes[move].legal == 1):
                            self.open_list.append(node.next_nodes[move])
                        if (self.checkIfDone(node.next_nodes[move].current_pos_cans) == 1):
                            self.addMove(move,node.next_nodes[move].with_can)
                            self.findroute(node)
                            result = 1
                    else:
                        node.next_nodes[move].legal = 0
                    
        print( "Current depth: " +str(current_depth)+ " Number of Nodes: " + str(number_of_nodes)+ " Elements in maps_tried: " + str(len(self.dictionary))+ " Elements in open_list: " + str(len(self.open_list)))
        print(self.route)
        print("Number of Steps: "+ str(len(self.route)))

    def find_score(self,node):

        score =  node.depth
        score += min([math.sqrt((pos_cans[0]-node.current_postion[0])**2+(pos_cans[1]-node.current_postion[1])**2) for pos_cans in node.current_pos_cans])
        
        for pos_cans in node.current_pos_cans:
            score += min([math.sqrt((pos_cans[0]-goal_pos[0])**2+(pos_cans[1]-goal_pos[1])**2) for goal_pos in self.map.pos_goal])
        # for pos_cans in node.current_pos_cans:
        #     shortest_dis = 100000
        #     dist = math.sqrt((pos_cans[0]-node.current_postion[0])**2+(pos_cans[1]-node.current_postion[1])**2)
        #     #dist = abs(pos_cans[0]-goal_pos[0])+abs(pos_cans[1]-goal_pos[1])
        #     if dist < shortest_dis :
        #         shortest_dis = dist
        # score +=shortest_dis

        # for pos_cans in node.current_pos_cans:
        #     shortest_dis = 100000
        #     for goal_pos in self.map.pos_goal:
        #         dist = math.sqrt((pos_cans[0]-goal_pos[0])**2+(pos_cans[1]-goal_pos[1])**2)
        #         #dist = abs(pos_cans[0]-goal_pos[0])+abs(pos_cans[1]-goal_pos[1])
        #         if dist < shortest_dis :
        #             shortest_dis = dist
        #             if(pos_cans == goal_pos):
        #                 score += -1
        #     score +=shortest_dis
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

    def A_star(self):

        first_node = nodes(None,self.map.pos_init,5,self.map.pos_cans,0)
        node_temp_current_pos = []
        node_temp_cans_pos = []
        global number_of_nodes
        number_of_nodes = 0
        result = 0
        current_depth = 0
        #self.open_list.append(first_node)
        heappush(self.open_list,(1.,id(first_node),first_node))
        while(len(self.open_list) >0 and result != 1 ):
            node = heappop(self.open_list)[2]#self.open_list.pop(0)
            #node = self.open_list.pop(0)
            #print("Current depth: " +str(current_depth)+ " Number of Nodes: " + str(number_of_nodes)+ " Elements in maps_tried: " + str(len(self.dictionary))+ " Elements in open_list: " + str(len(self.open_list))+" Current score: " +str(node.score))
            result = 0
            if(node.legal == 1):
                current_depth = node.depth 
                node_temp_current_pos = list(node.current_postion)
                for move in range(len(self.possible_steps)):
                    node_temp_cans_pos = list(node.current_pos_cans)
                    
                    node.next_nodes.append(nodes(node,node_temp_current_pos,move,node_temp_cans_pos,node.depth+1))
                    number_of_nodes = number_of_nodes + 1
                    is_legal = self.legalMove(move,node.next_nodes[move])

                    if(is_legal > 0):
                        self.updateMap(move,node.next_nodes[move],is_legal-1)
                        self.checkIftried(node.next_nodes[move])
                        node.next_nodes[move].with_can = is_legal-1
                        if node.next_nodes[move].legal == 1:
                            self.find_score(node.next_nodes[move])
                            heappush(self.open_list,(node.next_nodes[move].score,id(node.next_nodes[move]) , node.next_nodes[move]))
                        if (self.checkIfDone(node.next_nodes[move].current_pos_cans) == 1):
                            self.addMove(move,node.next_nodes[move].with_can)
                            self.findroute(node)
                            result = 1
                    else:
                        node.next_nodes[move].legal = 0
                    
                    
             
        print("Current depth: " +str(current_depth)+" Current score: " +str(node.score)+ " Number of Nodes: " + str(number_of_nodes)+ " Elements in maps_tried: " + str(len(self.dictionary))+ " Elements in open_list: " + str(len(self.open_list)))
        print(self.route)
        print("Number of Steps "+ str(len(self.route)))
