import pygame
from typing import List
import os

def select_screen(screen: pygame.Surface, screen_width: int, screen_height: int):

    pygame.font.init()

    musics: List[str] = music_list()

    #Define selection buttons particulars
    button_width = 400
    button_height = 50
    padding = 20
    top_offset = 120

    buttons = []
    for i, music in enumerate(musics):
        x = (screen_width - button_width) // 2
        y = top_offset + i * (button_height + padding)
        rect = pygame.Rect(x, y, button_width, button_height)
        buttons.append((music, rect))

    #Return
    return_rect = pygame.Rect(40, 600, 150, 40)

    while True:
        screen.fill((10, 10, 10))
        
        #Subtitle
        title_font = pygame.font.SysFont(None, 40)

        select_msg = title_font.render("Selecione uma Música", False, (255, 255, 255))
        select_pos = (40, 60)

        screen.blit(select_msg, select_pos)

        #Music Selection
        musics_font = pygame.font.SysFont(None, 30)

        for music, rect in buttons:
            pygame.draw.rect(screen, (50, 50, 50), rect)
            text = musics_font.render(music, True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        #Return Button
        pygame.draw.rect(screen, (80, 80, 80), return_rect)
        screen.blit(musics_font.render("Voltar", True, (255, 255, 255)), (return_rect.x + 10, return_rect.y + 5))

        #Display Update
        pygame.display.flip()

        #Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if return_rect.collidepoint(event.pos):
                    return ("menu", None)
                
                for music, rect in buttons:
                    if rect.collidepoint(event.pos):
                        return ("game", music)
                

def music_list() -> List[str]:
    mapped_music_path: str = "mapped_music/"

    musics: List[str] = []

    for music in os.listdir(mapped_music_path):
        path_music = os.path.join(mapped_music_path, music)

        if os.path.isdir(path_music):
            music_name = music.split("_")[1]
            musics.append(music_name)


    return musics
