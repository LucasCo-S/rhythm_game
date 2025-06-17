import pygame
import time
import queue
import threading
import input
import collision
from pygame.locals import *
from sys import exit
import notes
import interface
from typing import List
import music

pygame.init()

screen_width: int = 1280
screen_height: int = 720

#criação da tela
screen = pygame.display.set_mode((screen_width, screen_height))

#Time handle
FPS:int = 100
clock = pygame.time.Clock()

#titulo e icone 
pygame.display.set_caption("Rhythm Game")
icon = pygame.image.load('images/logo_img.png')
pygame.display.set_icon(icon)

#Input settings
key_label = {}
input_keys = [pygame.K_a, pygame.K_s, pygame.K_k, pygame.K_l]

input_data = queue.Queue()#Send to thread
input_info = queue.Queue()#Receive from thread

t_input_listen = threading.Thread(target = input.input_listen, args=(input_data, input_info), daemon = True) #daemon serve para finalizar a thread quando finaliza o programa
t_input_listen.start()

#Notes settings
note_data = queue.Queue()#Send to thread
note_info = queue.Queue()#Receive thread

selected_music = interface.user_input()
notes.notes_generator(selected_music, note_data)

interval_notes = []
screen_notes: List[notes.Note] = []

def get_interval_notes():
    while not note_data.empty():
        note: notes.Note = note_data.get()
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


sent_notes = set()

def draw_notes(delta_time: float):
    for note in screen_notes:
        note_rect = note.surf.get_rect(midbottom = (note.pos_x, note.pos_y))
        note.fall_note(delta_time)
        screen.blit(note.surf, note_rect)

        note_id = id(note)
        if (note.pos_y > 600 and note.pos_y < 750 and note_id not in sent_notes):
            note_info.put(note)
            sent_notes.add(note_id)

    # Remove notes out of screen
    screen_notes[:] = [note for note in screen_notes if note.pos_y < screen_height + note.size[1]]


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

    hit_pos_y: int = screen_height - 50
    one_rect = key_one.get_rect(midbottom = (200, hit_pos_y))  # Posição fixa para zona de acerto
    two_rect = key_two.get_rect(midbottom = (400, hit_pos_y))
    three_rect = key_three.get_rect(midbottom = (600, hit_pos_y))
    four_rect = key_four.get_rect(midbottom = (800, hit_pos_y))

    screen.blit(key_one, one_rect)
    screen.blit(key_two, two_rect)
    screen.blit(key_three, three_rect)
    screen.blit(key_four, four_rect)

    pygame.draw.line(screen, (255, 255, 255), (0, 675), (1200, 675), 2)


#Music Settings
"""
[0] playing
[1] unpause
[2] pause
"""
music_status: int = 0
music.music_init(selected_music)

#Collision settings
collision_info = queue.Queue() #Collision received data

t_collision_tester = threading.Thread(target = collision.collision_tester, args = (input_info, note_info, collision_info), daemon = True)
t_collision_tester.start()


#Loop Principal
loop_startTime: int = int(time.perf_counter() * 1000)
tolerance: int = 8

get_interval_notes() #Rendering all intervals

while True:
    current_time: float = float(time.perf_counter() * 1000) - loop_startTime
    
    #Delta time
    delta_time = clock.tick(FPS)

    screen.fill((28, 28, 28))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        #Music Control Status
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if music_status == 0:
                music_status = 2
                music.music_controller(music_status= music_status)
            else:
                music_status = 1
                music.music_controller(music_status= music_status)
                music_status = 0

     #ação de clicar e soltar a tecla
        if event.type == pygame.KEYDOWN and event.key in input_keys:
            key_label[event.key] = current_time

        if event.type == pygame.KEYUP and event.key in input_keys:
            input_start_time = key_label.pop(event.key, None)

            if input_start_time is not None:
                input_end_time = time.perf_counter()

                input_data.put((event.key, input_start_time, input_end_time))

    #Note geration
    spawn_notes(current_time, tolerance)

    #Rendering notes
    draw_notes(delta_time)

    draw_hitbox()

    pygame.display.flip()
    


