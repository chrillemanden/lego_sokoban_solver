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

        self.window_width = grid_size[0] * self.tile_size
        self.window_height = grid_size[1] * self.tile_size

        pygame.init()
        self.display = pygame.display.set_mode((self.window_width, self.window_height))

    def draw_grid(self):
        for row in range(self.grid_size[1]):
            for col in range(self.grid_size[0]):
                pygame.draw.rect(self.display, BLACK,[col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size],1)

    def update(self,environment,node):
        self.display.fill(WHITE)
        self.draw_grid()

        for row in range(self.grid_size[1]):
            for col in range(self.grid_size[0]):
                el = environment.map[row][col]
                if el == 'X':
                    pygame.draw.rect(self.display, GREY, [col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size])
                elif el == 'J':
                    pygame.draw.rect(self.display, RED, [col * self.tile_size + self.tile_size * 0.1, row * self.tile_size + self.tile_size * 0.1, self.tile_size * 0.8, self.tile_size * 0.8])
                elif el == 'G':
                    pygame.draw.rect(self.display, GREEN, [col * self.tile_size + self.tile_size * 0.1, row * self.tile_size + self.tile_size * 0.1, self.tile_size * 0.8, self.tile_size * 0.8])
                elif el == 'M':
                    pygame.draw.circle(self.display, PURPLE, (int(col * self.tile_size + 0.5 * self.tile_size), int( row * self.tile_size + 0.5 * self.tile_size)),int( self.tile_size * 0.3))
                    #pygame.draw.rect(self.display, GREEN, [col * self.tile_size + self.tile_size * 0.1, row * self.tile_size + self.tile_size * 0.1, self.tile_size * 0.8, self.tile_size * 0.8])

        #col = node.current_pos[0]
        #row = node.current_pos[1]
        #pygame.draw.circle(self.display, PURPLE, (col * self.tile_size + 0.5 * self.tile_size, row * self.tile_size + 0.5 * self.tile_size), self.tile_size * 0.3)

        pygame.display.update()
    
    def runRoute(self,node,Route):
        self.draw_grid

        f = open("Route.txt", "r")
        route = f.read()
        f.close()

        for i in range(len(route)):
            self.update(node.current_map,node)
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
            
            Route.updateMap(move,node,with_can)
            

            time.sleep(0.1)
        self.update(node.current_map,node)