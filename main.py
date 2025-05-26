# Importa a biblioteca Pygame, que fornece funcionalidades para criar jogos
import pygame
import time
import queue
import threading
import input
# Importa todas as constantes do Pygame que nos ajudam a detectar:
# - Teclas pressionadas (K_UP, K_DOWN, K_LEFT, K_RIGHT, etc)
# - Cliques do mouse (MOUSEBUTTONDOWN, MOUSEBUTTONUP)
# - Movimento do mouse (MOUSEMOTION)
# - Eventos da janela (QUIT, VIDEORESIZE)
# - Eventos do sistema (KEYDOWN, KEYUP)
from pygame.locals import *

# Importa a função exit() do módulo sys para encerrar o programa de forma limpa
from sys import exit

pygame.init()

screen_width: int = 1280
screen_height: int = 720

#criação da tela
screen = pygame.display.set_mode((screen_width, screen_height))

#Time handle
FPS:int = 60
clock = pygame.time.Clock()

#titulo e icone 
pygame.display.set_caption("Rhythm Game")
icon = pygame.image.load('images/logo_img.png')
pygame.display.set_icon(icon)

#Input settings
key_label = {}
input_keys = [pygame.K_a, pygame.K_s, pygame.K_k, pygame.K_l]

input_data = queue.Queue()
input_info = queue.Queue()

t_input_listen = threading.Thread(target = input.input_listen, args=(input_data, input_info), daemon = True)
t_input_listen.start()

#Loop principal
while True:

    # Esquema de coloração da tela(RGB)
    screen.fill((28, 28, 28))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

     #ação de clicar e soltar a tecla
        if event.type == pygame.KEYDOWN and event.key in input_keys:
            key_label[event.key] = time.perf_counter()

        if event.type == pygame.KEYUP and event.key in input_keys:
            input_start_time = key_label.pop(event.key, None)

            if input_start_time is not None:
                input_end_time = time.perf_counter()

                input_data.put((event.key, input_start_time, input_end_time))
    
    clock.tick(FPS)
    pygame.display.flip()
    


