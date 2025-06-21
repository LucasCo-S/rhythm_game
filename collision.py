import pygame
import queue
import time
import notes
import input
import threading
from typing import List

# Class to share time through threads
class SharedTime:
    def __init__(self):
        self._time = 0.0
        self._lock = threading.Lock()
    
    def update(self, new_time):
        with self._lock:
            self._time = new_time
    
    def get(self):
        with self._lock:
            return self._time

# Classify collision status from notes and inputs matched
class Collision_Record:
    def __init__(self, note: notes.Note, input: input.Input):
        self.precision = None
        self.type = note.type_note 
        self.points = None

# Thread that receive data from main
def collision_tester(input_info: queue.Queue, note_info: queue.Queue, collision_info: queue.Queue, shared_time: SharedTime):

    #Lists with inputs and notes values
    readed_inputs: List[input.Input] = []
    readed_notes: List[notes.Note] = []

    while True:
        # Get current time
        game_time: float = shared_time.get()
        
        # Collect NEW data from queues
        new_inputs: List[input.Input] = []
        while not input_info.empty():
            try:
                input_r: input.Input = input_info.get_nowait()
                new_inputs.append(input_r)
                readed_inputs.append(input_r)
            except queue.Empty:
                break

        while not note_info.empty():
            try:
                note_r: notes.Note = note_info.get_nowait()
                readed_notes.append(note_r) 
            except queue.Empty:
                break
        
        hit_collision(readed_inputs, readed_notes, new_inputs, collision_info)

        #Clean up both lists before collision checking
        cleanLists(readed_inputs, readed_notes, game_time)

        time.sleep(0.01)

# Identify collision from hold and tap notes
def hit_collision(readed_inputs: List[input.Input], readed_notes: List[notes.Note], new_inputs: List[input.Input], collision_info: queue.Queue):
    keys_label = {
        pygame.K_a: 200,
        pygame.K_s: 400,
        pygame.K_k: 600,
        pygame.K_l: 800
    }

    interval_hit = 1000
    tolerance_duration = 200
    
    for input_ in new_inputs:
        if input_.reached:
            continue
        for note_ in readed_notes:
            if note_.reached:  # Skip already hit notes
                continue
                
            delta_start_time = abs(input_.start - note_.hit_time)

            if note_.type_note != 128:
                if delta_start_time < interval_hit and keys_label[input_.key] == note_.pos_x:
                    input_.reached = True
                    note_.reached = True

                    print(">> Colidiu!")
                    break 
            else:
                delta_duration_time = abs(input_.duration - note_.duration)

                if delta_start_time < interval_hit and keys_label[input_.key] == note_.pos_x and delta_duration_time < tolerance_duration:
                    input_.reached = True
                    note_.reached = True
                    print("<<Colidiu!")
                    break
            
            #Send to collision class to classify hit
            collision_hit = Collision_Record(note_, input_)
            collision_info.put(collision_hit)

# Clean lists to ensure the data is relevant
def cleanLists(inputs_list: List[input.Input], notes_list: List[notes.Note], game_time: float):
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
    inputs_list[:] = [input for input in inputs_list if (game_time - input.end) < limit_time]
    notes_list[:] = [note for note in notes_list if (game_time - note.end_time) < limit_time]
    
    #Excluding if it's has been processed
    inputs_list[:] = [input for input in inputs_list if not input.reached]