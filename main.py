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

shared_time = collision.SharedTime() #Send current time for collision

#Const display
hit_pos_y: int = screen_height - (screen_height * 0.15)
note_travel_time: int = 1000 #One second

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

def spawn_notes(game_time: int, tolerance: int):
    i = 0
    while i < len(interval_notes):
        note_time, note = interval_notes[i]
        if abs(note_time - game_time) < tolerance:
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
        if (note.pos_y > (hit_pos_y - 50) and note.pos_y < (hit_pos_y + 50) and note_id not in sent_notes):
            note_info.put(note)
            sent_notes.add(note_id)

    # Remove notes out of screen
    screen_notes[:] = [note for note in screen_notes if note.pos_y < screen_height + note.size[1]]


#Notes hitbox
def draw_hitbox():
    pygame.draw.line(screen, (255, 255, 255), (0, hit_pos_y), (1200, hit_pos_y), 2)


#Music Settings
"""
[0] play
[1] unpause
[2] pause
"""
music_status: int = 0
music_playing: bool = False 
music.music_init(selected_music)

#Collision settings
collision_info = queue.Queue() #Collision received data

t_collision_tester = threading.Thread(target = collision.collision_tester, args = (input_info, note_info, collision_info, shared_time), daemon = True)
t_collision_tester.start()


#Loop Principal and PreLoads
get_interval_notes() #Rendering all intervals

tolerance: int = 8
game_time: float = 0.0

if interval_notes[0][0] - note_travel_time < 0: #Sleep the music until the note travel the needed time
    music_delay = abs(interval_notes[0][0] - note_travel_time)

else:
    music_delay = 0

clock.tick(FPS)  #Define game ticks by FPS

game_start_time = time.perf_counter()  #Absolute loop start time

while True:
    delta_time = clock.tick(FPS) # Return the time value of last call
    
    current_time = time.perf_counter()
    game_time = (current_time - game_start_time) * 1000

    shared_time.update(game_time)

    screen.fill((28, 28, 28))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        #Music Control Status
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if music_playing:
                music_status = 2
                music.music_controller(music_status)
                music_playing = False
            else:
                music_status = 1
                music.music_controller(music_status)
                music_playing = True  # CORREÇÃO: era music_status = True

        #Input Reading
        if event.type == pygame.KEYDOWN and event.key in input_keys:
            key_label[event.key] = game_time

        if event.type == pygame.KEYUP and event.key in input_keys:
            input_start_time = key_label.pop(event.key, None)

            if input_start_time is not None:
                input_end_time = game_time  # CORREÇÃO: usar game_time ao invés de time.perf_counter()
                input_data.put((event.key, input_start_time, input_end_time))

    #Music Initialization and Delay
    if game_time >= music_delay and not music_playing:
        music.music_controller(music_status)
        music_playing = True
    
    #Note geration
    spawn_notes(game_time, tolerance)

    #Rendering notes
    draw_notes(delta_time)

    draw_hitbox()

    pygame.display.flip()