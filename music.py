import queue
import os
import shutil
import notes
import pygame
from pathlib import Path

def readchart_files(file_path: str, music_path: str):
    #Read and Storing Notes
    with open(file_path, "r", encoding = "utf-8") as file:
        file_lines = file.readlines()
    
    index_chart = None
    for i, line in enumerate(file_lines):
        if(line.strip() == "[HitObjects]"):
            index_chart = i
            break

    if index_chart == None:
        raise ValueError("Cannot find Hit Objects in this file.")
    
    notes_queue = queue.Queue()
    file_lines = file_lines[index_chart + 1:]

    for line in file_lines:
        str_notes = line.split(',')

        if len(str_notes) < 5:
            raise ValueError("File integrity failure.")
        
        end_time = str_notes[5].split(':')[0] if str_notes[3] == "128" else str_notes[2]

        note = notes.Note(str_notes[0], str_notes[1], str_notes[2], str_notes[3], end_time)
        note.adjust_pos()

        notes_queue.put(note)

    #Creating a new chart file
    mapped_file = input("Digite o nome da música.\n")
    mapped_file += ".txt"

    with open(mapped_file, "w") as file:
        file.write("pos_x,pos_y,hit_time,type_note,end_time\n")

        while not notes_queue.empty():
            note: notes.Note = notes_queue.get()
            file.write(f"{note.pos_x},{note.pos_y},{note.hit_time},{note.type_note},{note.end_time}\n")

    #Create Folders
    os.makedirs("mapped_music", exist_ok=True)
    map_folder = f"map_{Path(mapped_file).stem}"
    os.makedirs(map_folder, exist_ok=True)
    
    #New music name
    music_ext = Path(music_path).suffix
    music_name = f"m_{Path(mapped_file).stem}{music_ext}"

    #Move files to new folder
    new_music_path = os.path.join(map_folder, music_name)
    shutil.move(music_path, new_music_path)
    
    shutil.move(mapped_file, map_folder)
    
    #Move entire folder to mapped_music
    shutil.move(map_folder, "mapped_music")


def music_init(music_name: str):
    path_music: str = os.path.join("mapped_music",f"map_{music_name}",f"m_{music_name}.mp3")

    if not os.path.exists(path_music):
        raise FileNotFoundError(f"Arquivo de música não encontrado: {path_music}")

    pygame.mixer.init()
    pygame.mixer.music.load(path_music)
    pygame.mixer.music.play() 

def music_controller(music_status: int):
    if music_status == 1:
        pygame.mixer.music.unpause()

    elif music_status == 2:
        pygame.mixer.music.pause()