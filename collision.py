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
        with self._lock: #Semaphorization
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
            500: "PERFECT",
            700: "GREAT", 
            1000: "GOOD",
            1500: "BAD",
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
        if precision <= 500:
            self.precision = precision_label[500]  # PERFECT
        elif precision <= 700:
            self.precision = precision_label[700]  # GREAT
        elif precision <= 1000:
            self.precision = precision_label[1000]  # GOOD
        elif precision <= 1500:
            self.precision = precision_label[1500]  # BAD
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
        
        #Process collisions - ordem alterada para evitar conflitos
        process_collisions(readed_inputs, readed_notes, collision_info, keys_label, shared_time)
        
        #Limpar notas perdidas DEPOIS do processamento de colisões
        missed_notes(readed_notes, collision_info, shared_time)

        #Clean up both lists DEPOIS de todo o processamento
        cleanLists(readed_inputs, readed_notes, shared_time)

        time.sleep(0.00005)  # Reduzido para melhor responsividade

def process_collisions(readed_inputs, readed_notes, collision_info: queue.Queue, keys_label, shared_time):
    game_time = shared_time.get()

    # Organizar notas por coluna
    notes_by_column = {}
    for note in readed_notes:
        if note.reached:
            continue
        col = note.pos_x
        if col not in notes_by_column:
            notes_by_column[col] = []
        notes_by_column[col].append(note)

    # Ordenar notas por proximidade do tempo de acerto
    for col_notes in notes_by_column.values():
        col_notes.sort(key=lambda n: abs(n.hit_time - game_time))

    # Verificar cada input
    for input_ in readed_inputs:
        if input_.reached:
            continue

        col = keys_label.get(input_.key)
        if col not in notes_by_column:
            continue

        possible_notes = notes_by_column[col]

        for note in possible_notes:
            if note.reached:
                continue

            delta = abs(input_.start - note.hit_time)
            if delta <= 3000 and match_tester(input_, note):
                create_collision(input_, note, collision_info)
                break  # um input só colide com uma nota



def missed_notes(readed_notes, collision_info: queue.Queue, shared_time):
    game_time = shared_time.get()

    """Processa notas perdidas"""
    miss_tolerance = 1000  # Tempo após o hit_time para considerar MISS
    
    for note in readed_notes:
        if note.reached:
            continue

        # Só considera MISS se o tempo atual passou do tempo de hit + tolerância
        # E a nota ainda não foi tocada
        time_since_hit = game_time - note.hit_time
        
        if time_since_hit > miss_tolerance:  # Passou do tempo + tolerância
            fail_input = inputs.Input(note.pos_x, note.hit_time, note.hit_time)
            fail_input.reached = True
            note.reached = True

            miss_record = Collision_Record(note, fail_input)
            miss_record.precision = "MISS"
            miss_record.points = 0
            miss_record.delta_precision = time_since_hit

            collision_info.put(miss_record)
            
            note_type = "HOLD" if note.type_note == 128 else "TAP"
            print(f">> {note_type} MISS! Time since hit: {time_since_hit}ms")

def match_tester(input_: inputs.Input, note: notes.Note) -> bool:
    """Testa se input e nota são compatíveis"""
    delta_time = abs(input_.start - note.hit_time)
    if delta_time > 3000:  # Tolerância para hit
        return False

    # Para notas hold, verificar também a duração
    if note.type_note == 128:
        duration_delta = abs(input_.duration - note.duration)
        if duration_delta > 3000:  # Tolerância para duração
            return False

    return True

def create_collision(input_: inputs.Input, note: notes.Note, collision_info: queue.Queue):
    """Cria um registro de colisão"""
    input_.reached = True
    note.reached = True

    collision_hit = Collision_Record(note, input_)
    collision_hit.compute_precision()
    collision_hit.compute_points()

    collision_info.put(collision_hit)

    note_type = "HOLD" if note.type_note == 128 else "TAP"
    print(f">> {note_type} Hit! Precision: {collision_hit.precision} ({collision_hit.delta_precision}ms)")


def cleanLists(inputs_list: List[inputs.Input], notes_list: List[notes.Note], shared_time):
    game_time = shared_time.get()
    """Limpa listas removendo elementos muito antigos ou já processados"""
    
    # Tempo limite para manter elementos na memória
    limit_time: float = 2000.0  # Aumentado para 2 segundos
    
    # Remover inputs muito antigos ou já processados
    inputs_list[:] = [
        input for input in inputs_list 
        if (game_time - input.end) < limit_time and not input.reached
    ]
    
    # Remover notas muito antigas ou já processadas
    notes_list[:] = [
        note for note in notes_list 
        if abs(note.hit_time - game_time) < limit_time and not note.reached
    ]