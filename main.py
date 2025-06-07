import pygame
import time
import queue
import threading
import input
from pygame.locals import *
from sys import exit
import notes
import interface
from typing import List

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

#Read and Initialization
note_order = queue.Queue()
note_queue = queue.Queue() #Recycle values from note_order

selected_music = interface.user_input()
notes.notes_generator(selected_music, note_order)

interval_notes = []
screen_notes: List[notes.Note] = []

def get_interval_notes():
    while not note_order.empty():
        note: notes.Note = note_order.get()
        interval_notes.append((note.hit_time, note))

def spawn_notes(current_time: int, tolerance: int):
    i = 0
    while i < len(interval_notes):
        note_time, note = interval_notes[i]
        if abs(note_time - current_time) < tolerance:
            screen_notes.append(note)
            interval_notes.pop(i)
        else:
            i += 1

def draw_notes():
    for note in screen_notes:
        note_rect = note.surf.get_rect(midbottom = (note.pos_x, note.pos_y))
        note.fall_note()
        screen.blit(note.surf, note_rect)
    
    # Remove notas que saíram da tela
    screen_notes[:] = [note for note in screen_notes if note.pos_y < screen_height + note.size[1]]

    
#Loop Principal
loop_startTime: int = int(time.perf_counter() * 1000)
tolerance: int = 12

get_interval_notes() #Rendering all intervals

#Notes hitbox
def draw_hitbox():
    key_one = pygame.Surface((100, 50))
    key_two = pygame.Surface((100, 50))
    key_three = pygame.Surface((100, 50))
    key_four = pygame.Surface((100, 50))

    key_one.fill('Orange')
    key_two.fill('Green')
    key_three.fill('Blue')
    key_four.fill('Purple')

    one_rect = key_one.get_rect(midbottom = (200, 700))  # Posição fixa para zona de acerto
    two_rect = key_two.get_rect(midbottom = (400, 700))
    three_rect = key_three.get_rect(midbottom = (600, 700))
    four_rect = key_four.get_rect(midbottom = (800, 700))

    screen.blit(key_one, one_rect)
    screen.blit(key_two, two_rect)
    screen.blit(key_three, three_rect)
    screen.blit(key_four, four_rect)

    pygame.draw.line(screen, (255, 255, 255), (0, 675), (1200, 675), 2)

while True:
    current_time: int = int(time.perf_counter() * 1000) - loop_startTime

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

    #Note geration
    spawn_notes(current_time, tolerance)

    #Rendering notes
    draw_notes()

    draw_hitbox()

    clock.tick(FPS)
    pygame.display.flip()
    


