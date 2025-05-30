import pygame
import time
import queue
import threading
import input
from pygame.locals import *
from sys import exit
import notes

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

t_input_listen = threading.Thread(target = input.input_listen, args=(input_data, input_info), daemon = True) #daemon serve para finalizar a thread quando finaliza o programa
t_input_listen.start()

#Notes settings
note_data = queue.Queue()

note_info = queue.Queue()

note_listen = threading.Thread(target= notes.note_generation, args=(note_data, note_info), daemon=True)

#Loop principal
while True:
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
    


