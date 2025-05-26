import pygame
import queue

class Note:
    def __init__(self):
        self.size = (70, 50)
        self.pos_x = None
        self.pos_y = 0

        #Note Surface
        self.surf = pygame.Surface((self.size))
        self.surf.fill('Red')
        
