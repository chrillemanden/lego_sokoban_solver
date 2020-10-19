
class map:
    def __init__(self, location):
        self.map_location = location
        self.map = []
        self.pos_goal = []
        self.pos_init = []
        self.pos_cans = []
    
    def printMap(self):
        print(self.map_location)
        for lines in self.map:
            print(lines)

    def findObjsInMap(self): 
                        #(X: walls; .: paths;
                        # G: goal positions of cans; 
                        # M: initial position of robot; 
                        # J: initial positions of cans):
        for lines in range(len(self.map)):
            for elements in range(len(self.map[lines])):
                if (self.map[lines][elements] == 'G') : 
                    self.pos_goal.append( [lines , elements])
                elif (self.map[lines][elements] == 'M') : 
                    self.pos_init = [lines , elements]
                elif (self.map[lines][elements] == 'J') : 
                    self.pos_cans.append( [lines , elements])

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
                

        