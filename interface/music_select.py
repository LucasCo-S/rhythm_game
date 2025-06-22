import pygame

def select_screen(screen, screen_width, screen_height):

    pygame.font.init()

    while True:
       
        #Display Update
        pygame.display.flip()

        #Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
