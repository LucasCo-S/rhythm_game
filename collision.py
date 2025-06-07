import pygame
import queue
import time
import notes
import input

def collision_tester(input_info: queue.Queue, note_info: queue.Queue, collision_info: queue.Queue):
    while True:
        # Verifica se chegaram dados de input
        while not input_info.empty():
            try:
                inputs: input.Input = input_info.get_nowait()
            except queue.Empty:
                break
        
        # Verifica se chegaram dados de notas
        while not note_info.empty():
            try:
                note: notes.Note = note_info.get_nowait()
            except queue.Empty:
                break
        
        tolerance = 60

        # 10 se start >= 10 - 60 && start <= 10 + 60
    
        # Pequena pausa para não sobrecarregar
        time.sleep(0.01)