import pygame

def menu_screen(screen, screen_width, screen_height):

    pygame.font.init()

    while True:
        screen.fill((10, 10, 10))
        
        #Game title
        font = pygame.font.SysFont(None, 72)

        title = font.render("Rhyphos", True, (255, 255, 255))
        title_pos = (screen_width // 2 - title.get_width() // 2, 150) #'//' Return a integer valur

        screen.blit(title, title_pos)

        #Selection buttons
        font_small = pygame.font.SysFont(None, 48)

        #Play button
        play_button = font_small.render("Iniciar", True, (200, 200, 200))
        play_rect = play_button.get_rect(center = (screen_width // 2, 300))
        
        pygame.draw.rect(screen, (70, 70, 70), play_rect.inflate(20, 10))

        screen.blit(play_button, play_rect)

        #Settings button
        settings_button = font_small.render("Configurações", True, (200, 200, 200))
        settings_rect = settings_button.get_rect(center = (screen_width // 2, 450))
        
        pygame.draw.rect(screen, (70, 70, 70), settings_rect.inflate(20, 10))

        screen.blit(settings_button, settings_rect)

        #Exit button
        exit_button = font_small.render("Sair", True, (200, 200, 200))
        exit_rect = exit_button.get_rect(center = (screen_width // 2, 600))
        
        pygame.draw.rect(screen, (70, 70, 70), exit_rect.inflate(20, 10))

        screen.blit(exit_button, exit_rect)


        #Display Update
        pygame.display.flip()

        #Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_rect.collidepoint(event.pos):
                    return 'select_music'
                
                if settings_rect.colliderect(event.pos):
                    return 'settings'
                
                if exit_rect.colliderect(event.pos):
                    return 'exit'
