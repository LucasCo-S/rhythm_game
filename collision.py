import pygame
import queue
import time
import notes
import input
from typing import List

# class Collision:
#     def __init__(self):

def collision_tester(input_info: queue.Queue, note_info: queue.Queue, collision_info: queue.Queue, actual_time: queue.Queue):
    game_time: float = actual_time.get()

    keys_label = {
        pygame.K_a : 200,
        pygame.K_s : 400,
        pygame.K_k : 600,
        pygame.K_l : 800
    }
        
    readed_inputs: List[input.Input] = []
    readed_notes: List[notes.Note] = []

    while True:
        # Verifica se chegaram dados de input
        while not input_info.empty():
            try:
                input_r: input.Input = input_info.get_nowait()
                readed_inputs.append(input_r)

            except queue.Empty:
                break
        
        # Verifica se chegaram dados de notas
        while not note_info.empty():
            try:
                note_r: notes.Note = note_info.get_nowait()
                readed_notes.append(note_r)

            except queue.Empty:
                break
    
        cleanLists(readed_inputs, readed_notes, game_time)

        interval_hit = 100 #In miliseconds
        for input_ in readed_inputs:
            for note_ in readed_notes:
                if abs(input_.start - note_.hit_time) < interval_hit and keys_label[input_.key] == note_.pos_x:
                    print("Colidiu")


def cleanLists(inputs_list: List[input.Input], notes_list: List[notes.Note], actual_time: float):
    keys_label = {
        pygame.K_a : 200,
        pygame.K_s : 400,
        pygame.K_k : 600,
        pygame.K_l : 800
    }
    
    #Excluding inputs if don't had any note in column
    inputs_list[:] = [input for input in inputs_list if any(note.pos_x == keys_label[input.key] for note in notes_list)]
    
    #Excluding items by time
    limit_time: float = 1500.0
    inputs_list[:] = [input for input in inputs_list if (actual_time - input.end) < limit_time]
    notes_list[:] = [note for note in notes_list if (actual_time - note.end_time) < limit_time]
    
    #Excluding if it's has been processed
    inputs_list[:] = [input for input in inputs_list if not input.reached]
        

        
        