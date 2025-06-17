import pygame
import queue
from pathlib import Path
import os

screen_width: int = 1280
screen_height: int = 720

fps: int = 100

class Note:
    def __init__(self, pos_x, pos_y, hit_time, type_note, end_time, travel_time=None):
        self.pos_x = int(pos_x)
        self.pos_y = int(pos_y)
        self.hit_time = int(hit_time)
        self.end_time = int(end_time)
        self.type_note = int(type_note)

        self.duration = int(self.end_time - self.hit_time) / 1000 #Converting to seconds
        self.speed = (screen_height - 50) / 1000 #velocity per milisecond

        if travel_time is not None:
            self.compute_size(travel_time)
        else:
            self.size = (100, 25)

        #Note Surface - criada APÓS calcular o tamanho
        self.surf = pygame.Surface(self.size)
        if self.end_time - self.hit_time == 0:
            self.surf.fill("Red")
        else:
            self.surf.fill("Blue")

    def adjust_pos(self):
        if self.pos_x == 64: self.pos_x = 200
        if self.pos_x == 192: self.pos_x = 400
        if self.pos_x == 320: self.pos_x = 600
        if self.pos_x == 448: self.pos_x = 800

        self.pos_y = 0

    def fall_note(self, delta_time: float):
        self.pos_y += self.speed * delta_time

    def compute_size(self, travel_time):
        if self.duration <= 0:
            self.size = (100, 25)
        else:
            calculated_height = int((self.duration / travel_time) * screen_height)
            self.size = (100, calculated_height)

        
    
def notes_generator(mapped_file: str, note_order: queue.Queue):
    path: str = os.path.join("mapped_music",f"map_{mapped_file}",f"{mapped_file}.txt")

    with open(path, "r") as file:
        file_lines = file.readlines()
    
    # Calcular travel_time uma vez só
    travel_time = (screen_height - 50) / 1000
    
    for line in file_lines:
        if line == "pos_x,pos_y,hit_time,type_note,end_time\n": continue

        else:
            str_line = line.strip().split(",")
            # PASSAR travel_time no construtor
            note = Note(str_line[0], str_line[1], str_line[2], str_line[3], str_line[4], travel_time)

            note_order.put(note)

