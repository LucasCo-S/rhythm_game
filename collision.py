import pygame
import queue
import time
import notes
import inputs
import threading
from typing import List

#Class to share time through threads
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

#Classify collision status from notes and inputs matched
class Collision_Record:
    def __init__(self, note: notes.Note, input: inputs.Input):
        self.note_info = note
        self.input_info = input
        self.precision = None
        self.type = note.type_note 
        self.points = None
        self.delta_precision = None

    
    def compute_precision(self):
        precision_label = {
            80: "PERFECT",
            100: "GREAT", 
            150: "GOOD",
            300: "BAD",
            -1: "MISS"
        }

        precision = abs(self.note_info.hit_time - self.input_info.start)
        
        #Debug
        print(f"DEBUG - Note hit_time: {self.note_info.hit_time}, Input start: {self.input_info.start}")
        print(f"DEBUG - Precision delta: {precision}")
        
        if self.type == 128:
            duration_precision = abs(self.note_info.duration - self.input_info.duration)
            precision = max(precision, duration_precision) #Return the greater error

        self.delta_precision = precision
        
        #Determine precision category based on timing difference
        if precision <= 80:
            self.precision = precision_label[80]  # PERFECT
        elif precision <= 100:
            self.precision = precision_label[100]  # GREAT
        elif precision <= 150:
            self.precision = precision_label[150]  # GOOD
        elif precision <= 300:
            self.precision = precision_label[300]  # BAD
        else:
            self.precision = precision_label[-1]  # MISS 
    
    def compute_points(self):
        points_label = {
            "PERFECT" : 500,
            "GREAT" : 300,
            "GOOD" : 100,
            "BAD" : 50,
            "MISS" : 0
        }

        self.points = points_label[self.precision]



#Thread that receive data from main
def collision_tester(input_info: queue.Queue, note_info: queue.Queue, collision_info: queue.Queue, shared_time: SharedTime, event_pause):

    #Lists with inputs and notes values
    readed_inputs: List[inputs.Input] = []
    readed_notes: List[notes.Note] = []

    notes_pos = [400, 550, 700, 850]
    keys_list = inputs.load_user_settings()
    keys_label = dict(zip(keys_list, notes_pos))

    while True:
        event_pause.wait() #Semaphorization
        
        game_time: float = shared_time.get()
        
        #Reading data from main
        new_inputs: List[inputs.Input] = []
        while not input_info.empty():
            try:
                input_r: inputs.Input = input_info.get_nowait()
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
        
        #Identify collision from hold and tap notes
        process_inputs(new_inputs, readed_notes, collision_info, keys_label)
        process_notes(readed_inputs, readed_notes, collision_info, keys_label, game_time)
        missed_notes(readed_notes, collision_info, game_time)

        #Clean up both lists before collision checking
        cleanLists(readed_inputs, readed_notes, game_time, keys_label)

        time.sleep(0.01)

def process_inputs(new_inputs, readed_notes, collision_info: queue.Queue, keys_label):
    for input_ in new_inputs:
        if input_.reached:
            continue

        column = keys_label[input_.key]
        candidate_notes = []
        for note in readed_notes:
            if note.reached or note.pos_x != column:
                continue

            delta_hit = abs(input_.start - note.hit_time)
            if delta_hit <= 300: #Tolerance to hit
                candidate_notes.append((note, delta_hit))

        if not candidate_notes:
            continue

        candidate_notes.sort(key=lambda x: x[1]) #Use the second tuple value to find the best note for collision
        best_note = candidate_notes[0][0]

        if match_tester(input_, best_note):
            create_collision(input_, best_note, collision_info)

def process_notes(readed_inputs, readed_notes, collision_info: queue.Queue, keys_label, game_time):
    perfect_window = 50

    for note in readed_notes:
        if note.reached:
            continue

        time_to_hit = abs(note.hit_time - game_time)
        if time_to_hit <= perfect_window:
            column = note.pos_x
            best_input = None
            best_delta = float('inf') #Receive a 'infinite' value 

            for input_ in readed_inputs:
                if input_.reached:
                    continue

                if keys_label[input_.key] != column:
                    continue

                delta = abs(input_.start - note.hit_time)
                if delta < best_delta and delta <= 300: #Tolerance to hit
                    best_input = input_
                    best_delta = delta

            if best_input and match_tester(best_input, note):
                create_collision(best_input, note, collision_info)

def missed_notes(readed_notes, collision_info: queue.Queue, game_time: float):
    for note in readed_notes:
        if note.reached:
            continue

        if game_time - note.hit_time > 300: #Tolerance to hit
            fail_input = inputs.Input(note.pos_x, note.hit_time, note.hit_time)
            fail_input.reached = True
            note.reached = True

            miss_record = Collision_Record(note, fail_input)
            miss_record.precision = "MISS"
            miss_record.points = 0
            miss_record.delta_precision = abs(note.hit_time - game_time)

            collision_info.put(miss_record)

def match_tester(input_: inputs.Input, note: notes.Note) -> bool:
    delta_time = abs(input_.start - note.hit_time)
    if delta_time > 300: #Tolerance to hit
        return False

    if note.type_note == 128:
        duration_delta = abs(input_.duration - note.duration)
        if duration_delta > 300:
            return False

    return True

def create_collision(input_: inputs.Input, note: notes.Note, collision_info: queue.Queue):
    input_.reached = True
    note.reached = True

    collision_hit = Collision_Record(note, input_)
    collision_hit.compute_precision()
    collision_hit.compute_points()

    collision_info.put(collision_hit)

    note_type = "HOLD" if note.type_note == 128 else "TAP"
    print(f">> {note_type} Hit! Precision: {collision_hit.precision} ({collision_hit.delta_precision}ms)")


# Clean lists to ensure the data is relevant
def cleanLists(inputs_list: List[inputs.Input], notes_list: List[notes.Note], game_time: float, keys_label):
    
    limit_time: float = 1000.0
    
    inputs_list[:] = [input for input in inputs_list if (game_time - input.end) < limit_time]
    
    notes_list[:] = [note for note in notes_list if (note.hit_time - game_time) > -limit_time and (note.hit_time - game_time) < limit_time]
    
    inputs_list[:] = [input for input in inputs_list if not input.reached]
    notes_list[:] = [note for note in notes_list if not note.reached]