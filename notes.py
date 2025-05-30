import pygame
import queue
import shutil
import os

class Note:
    def __init__(self, pos_x, pos_y, hit_time, type_note, end_time):
        self.pos_x = int(pos_x)
        self.pos_y = int(pos_y)
        self.hit_time = int(hit_time)
        self.end_time = int(end_time)
        self.type_note = int(type_note)

        #Note Surface
        self.surf = pygame.Surface((100,50))
        self.surf.fill('Red')


def readchart_files(file_path: str):
    #Read and Storing Notes
    with open(file_path, "r") as file:
        file_lines = file.readlines()
    
    index_chart = None
    for i, line in enumerate(file_lines):
        if(line.strip() == "[HitObjects]"):
            index_chart = i
            break

    if index_chart == None:
        raise ValueError("Cannot find Hit Objects in this file.")
    
    notes = queue.Queue()
    file_lines = file_lines[index_chart + 1:]

    for line in file_lines:
        str_notes = line.split(',')

        if len(str_notes) < 5:
            raise ValueError("File integrity failure.")
        
        end_time = str_notes[5].split(':')[0] if str_notes[3] == "128" else str_notes[2]

        note = Note(str_notes[0], str_notes[1], str_notes[2], str_notes[3], end_time)
        notes.put(note)

    #Creating a new chart file
    mapped_file = input("Digite o nome da música.\n")
    mapped_file += ".txt"

    with open(mapped_file, "w") as file:
        file.write("pos_x,pos_y,hit_time,type_note,end_time\n")

        while not notes.empty():
            note: Note = notes.get()
            file.write(f"{note.pos_x},{note.pos_y},{note.hit_time},{note.type_note},{note.end_time}\n")


    os.makedirs("mapped_music", exist_ok=True)
    shutil.move(mapped_file, f"mapped_music/{mapped_file}")