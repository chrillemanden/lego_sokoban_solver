import pygame
from route_class import nodes 
from route_class import route 
import time

WHITE = [255, 255, 255]
RED = [255, 0, 0]
BLACK = [0, 0, 0]
GREEN = [0, 255, 0]
GREY = [128,128,128]
PURPLE = [128,0,128]
ORANGE = [255,127,80]


class Display:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.tile_size = 80
        self.possible_steps= []
        self.possible_steps.append([1,0]) #DOWN
        self.possible_steps.append([-1,0]) #UP
        self.possible_steps.append([0,1]) #RIGHT
        self.possible_steps.append([0,-1]) #LEFT

        self.window_width = grid_size[0] * self.tile_size
        self.window_height = grid_size[1] * self.tile_size

        pygame.init()
        self.display = pygame.display.set_mode((self.window_width, self.window_height))

    def draw_grid(self):
        for row in range(self.grid_size[1]):
            for col in range(self.grid_size[0]):
                #pygame.draw.rect(self.display, BLACK,[col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size],1)
                pygame.draw.line(self.display, BLACK, (col*self.tile_size+40,row*self.tile_size), (col*self.tile_size+40,row*self.tile_size+80),5)
                pygame.draw.line(self.display, BLACK, (col*self.tile_size,row*self.tile_size+40), (col*self.tile_size+80,row*self.tile_size+40),5)

    def update(self,Route,node):
        self.display.fill(WHITE)
        self.draw_grid()

        for row in range(self.grid_size[1]):
            for col in range(self.grid_size[0]):
                el = Route.map.map_dictonary[str(row)+","+str(col)]
                if el == 0:
                    pygame.draw.rect(self.display, WHITE, [col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size])
        for goal in Route.map.pos_goal:
            pygame.draw.rect(self.display, GREEN, [goal[1] * self.tile_size + self.tile_size * 0.1, goal[0] * self.tile_size + self.tile_size * 0.1, self.tile_size * 0.8, self.tile_size * 0.8])
        for cans in node.current_pos_cans:
            pygame.draw.rect(self.display, RED, [cans[1] * self.tile_size + self.tile_size * 0.1, cans[0] * self.tile_size + self.tile_size * 0.1, self.tile_size * 0.8, self.tile_size * 0.8])
        
        pygame.draw.circle(self.display, PURPLE, (int(node.current_postion[1] * self.tile_size + 0.5 * self.tile_size), int( node.current_postion[0] * self.tile_size + 0.5 * self.tile_size)),int( self.tile_size * 0.3))

        pygame.display.update()
    
    def updateMap(self,move,node,with_can): # update the map
        new_pos = [node.current_postion[0]+self.possible_steps[move][0], node.current_postion[1]+self.possible_steps[move][1]]
        if (with_can == 1):
            new_pos_can = [new_pos[0]+self.possible_steps[move][0], new_pos[1]+self.possible_steps[move][1]]
            index = (node.current_pos_cans.index(new_pos))
            node.current_pos_cans[index] = new_pos_can
        node.current_postion = new_pos
    
    def runRoute(self,node,Route):
        self.draw_grid

        f = open("Route.txt", "r")
        route = f.read()
        f.close()

        for i in range(len(route)):
            self.update(Route,node)
            if (route[i].isupper()):
                with_can = 1
            else:  
                with_can = 0
            
            if route[i].lower() == 'd':
                move = 0
            elif route[i].lower() == 'u':
                move = 1
            elif route[i].lower() == 'r':
                move = 2
            elif route[i].lower() == 'l':
                move = 3
            
            self.updateMap(move,node,with_can)
            time.sleep(0.1)

        self.update(Route,node)
