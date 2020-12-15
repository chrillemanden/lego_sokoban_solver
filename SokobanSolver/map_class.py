
class map:
    def __init__(self, location):
        self.map_location = location
        self.map = []
        self.pos_goal = []
        self.pos_init = []
        self.pos_cans = []
        self.map_dictonary = {'Start': 1}
        self.loadMap()
    
    def printMap(self):
        print(self.map_location)
        for lines in self.map:
            print(lines)


    def printDict(self):
        for lines in range(len(self.map)):
            for elements in range(len(self.map[lines])):
                index = str(lines)+","+str(elements)
                print(self.map_dictonary[index], end =" ")  
            print(" ")    


    def findObjsInMap(self): 
                        #(X: walls; .: paths;
                        # G: goal positions of cans; 
                        # M: initial position of robot; 
                        # J: initial positions of cans):

        possible_steps = []
        possible_steps.append([1,0]) #DOWN
        possible_steps.append([-1,0]) #UP
        possible_steps.append([0,1]) #RIGHT
        possible_steps.append([0,-1]) #LEFT

        for lines in range(len(self.map)):
            for elements in range(len(self.map[lines])):
                if (self.map[lines][elements] == 'G') : 
                    self.pos_goal.append([lines , elements])
                    self.map_dictonary[str(lines)+","+str(elements)] = 1
                elif (self.map[lines][elements] == 'J') : 
                    self.pos_cans.append([lines , elements])
                    self.map_dictonary[str(lines)+","+str(elements)] = 1
                elif (self.map[lines][elements] == 'X') :
                    self.map_dictonary[str(lines)+","+str(elements)] = 0 
                elif (self.map[lines][elements] == '.' or self.map[lines][elements] == 'M') :
                    if(self.map[lines][elements] == 'M'):
                        self.pos_init = [lines,elements]
                    value = 1
                    for test_move in range(len(possible_steps)):
                        new_pos_temp = [lines+possible_steps[test_move][0], elements+possible_steps[test_move][1]]
                        if(self.map[new_pos_temp[0]][new_pos_temp[1]] == 'X'):
                            new_pos_down = [lines+possible_steps[0][0], elements+possible_steps[0][1]]
                            new_pos_up = [lines+possible_steps[1][0], elements+possible_steps[1][1]]
                            new_pos_right = [lines+possible_steps[2][0], elements+possible_steps[2][1]]
                            new_pos_left = [lines+possible_steps[3][0], elements+possible_steps[3][1]]
                            if(test_move == 0):
                                if (self.map[new_pos_left[0]][new_pos_left[1]] == 'X' or self.map[new_pos_right[0]][new_pos_right[1]] == 'X'):
                                    value = 2
                                    break
                            elif (test_move == 1):
                                if (self.map[new_pos_left[0]][new_pos_left[1]] == 'X' or self.map[new_pos_right[0]][new_pos_right[1]] == 'X') :
                                    value = 2
                                    break
                            elif(test_move == 2  ):
                                if(self.map[new_pos_up[0]][new_pos_up[1]] == 'X' or self.map[new_pos_down[0]][new_pos_down[1]] == 'X') :
                                    value = 2
                                    break
                            elif(test_move == 3 ):
                                if(self.map[new_pos_up[0]][new_pos_up[1]] == 'X' or self.map[new_pos_down[0]][new_pos_down[1]] == 'X') :
                                    value = 2
                                    break
                    self.map_dictonary[str(lines)+","+str(elements)] = value



    def loadMap(self):
        file = open(self.map_location,"r")
        temp = file.read().splitlines()
        temp_vertical = []
        for line in temp:
            for letters in line:
                temp_vertical.append(letters)
            self.map.append(temp_vertical)
            temp_vertical = []
        file.close()
        self.findObjsInMap()
                

        