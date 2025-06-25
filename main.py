#Libraries Imports
import pygame
import time
import queue
import threading
from pygame.locals import *
from sys import exit
from typing import List

#Modules Import
import inputs
import collision
import interface.game_score
import interface.menu
import interface.music_select
import interface.settings
import notes
import music
import interface

#Initilizing game
pygame.init()

#Screen Settings
screen_width: int = 1280
screen_height: int = 720

screen = pygame.display.set_mode((screen_width, screen_height))

#Time handle
FPS:int = 100
clock = pygame.time.Clock()

shared_time = collision.SharedTime() #Send current time for collision

#Hit settings
hit_pos_y: int = screen_height - (screen_height * 0.15)
note_travel_time: int = 1000 #One second

#Game Icon and Title
pygame.display.set_caption("Rhyphos")
icon = pygame.image.load('images/logo_img.png')
pygame.display.set_icon(icon)

#Input settings
key_label = {}

input_data = queue.Queue()#Send to thread
input_info = queue.Queue()#Receive from thread

t_input_listen = threading.Thread(target = inputs.input_listen, args=(input_data, input_info), daemon = True)
t_input_listen.start()

#Notes settings
note_data = queue.Queue()#Send to thread
note_info = queue.Queue()#Receive thread

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

# Visual styling class
class GameVisuals:
    def __init__(self):
        self.button_positions = [400, 550, 700, 850]
        self.button_colors = {
            400: (255, 80, 80),   # Red
            550: (80, 255, 80),   # Green  
            700: (80, 80, 255),   # Blue
            850: (255, 255, 80)   # Yellow
        }
        self.button_pressed = {pos: False for pos in self.button_positions}
        self.button_press_time = {pos: 0 for pos in self.button_positions}
    
    def create_gradient_background(self, surface):
        """Creates a smooth dark gradient background"""
        for y in range(screen_height):
            ratio = y / screen_height
            # Dark gradient from deep blue to purple
            r = int(20 + (35 - 20) * ratio)
            g = int(15 + (25 - 15) * ratio) 
            b = int(40 + (60 - 40) * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (screen_width, y))
    
    def draw_hitbox_buttons(self, surface, current_time):
        """Draws stylized buttons at note positions"""
        button_width = 90
        button_height = 50
        
        for pos_x in self.button_positions:
            # Check if button should be pressed
            is_pressed = self.button_pressed[pos_x]
            
            # Button colors
            base_color = self.button_colors[pos_x]
            
            if is_pressed:
                # Pressed state - brighter
                color = tuple(min(255, int(c * 1.3)) for c in base_color)
                border_color = (255, 255, 255)
            else:
                # Normal state - dimmer
                color = tuple(int(c * 0.6) for c in base_color)
                border_color = tuple(int(c * 0.8) for c in base_color)
            
            # Button rectangle
            button_rect = pygame.Rect(pos_x - button_width//2, hit_pos_y - button_height//2, 
                                    button_width, button_height)
            
            # Draw button shadow
            shadow_rect = pygame.Rect(button_rect.x + 2, button_rect.y + 2, 
                                    button_width, button_height)
            pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=8)
            
            # Draw button background
            pygame.draw.rect(surface, color, button_rect, border_radius=8)
            
            # Draw button border
            pygame.draw.rect(surface, border_color, button_rect, width=2, border_radius=8)
            
            # Draw inner glow when pressed
            if is_pressed:
                inner_rect = pygame.Rect(button_rect.x + 4, button_rect.y + 4,
                                       button_width - 8, button_height - 8)
                glow_color = tuple(min(255, int(c * 1.5)) for c in base_color)
                glow_surface = pygame.Surface((button_width - 8, button_height - 8), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (*glow_color, 80), glow_surface.get_rect(), border_radius=6)
                surface.blit(glow_surface, (inner_rect.x, inner_rect.y))
    
    def press_button(self, pos_x):
        """Activates button press effect"""
        if pos_x in self.button_pressed:
            self.button_pressed[pos_x] = True
    
    def release_button(self, pos_x):
        """Deactivates button press effect"""
        if pos_x in self.button_pressed:
            self.button_pressed[pos_x] = False

# Initialize visuals
game_visuals = GameVisuals()

def draw_stylized_hitbox():
    """Draws an enhanced hitbox line"""
    # Draw glowing hitbox line
    pygame.draw.line(screen, (100, 150, 255), (0, hit_pos_y), (screen_width, hit_pos_y), 4)
    pygame.draw.line(screen, (200, 220, 255), (0, hit_pos_y), (screen_width, hit_pos_y), 2)


#Music Settings
music_status: int
music_playing: bool

#Collision settings
collision_info = queue.Queue() #Collision received data

t_collision_tester = threading.Thread(target = collision.collision_tester, args = (input_info, note_info, collision_info, shared_time), daemon = True)
t_collision_tester.start()

#Principal Loop and PreLoads
clock.tick(FPS)  #Define game ticks by FPS

def game_loop(selected_music: str):
    notes.notes_generator(selected_music, note_data)
    music.music_init(selected_music)

    get_interval_notes()
    last_note = interval_notes[-1][0] if interval_notes else 0
    margin_end = 2000

    game_start_time = time.perf_counter()
    tolerance = 8
    music_playing = False
    music_status = 0

    if interval_notes[0][0] - note_travel_time < 0:
        music_delay = abs(interval_notes[0][0] - note_travel_time)
    else:
        music_delay = 0

    sent_notes.clear()
    screen_notes.clear()

    #Getting User Settings
    input_keys = inputs.load_user_settings()
    
    # Map input keys to button positions
    key_to_position = {}
    if len(input_keys) >= 4:
        positions = [400, 550, 700, 850]
        for i, key in enumerate(sorted(input_keys)[:4]):
            key_to_position[key] = positions[i]

    while True:
        delta_time = clock.tick(FPS)
        current_time = time.perf_counter()
        game_time = (current_time - game_start_time) * 1000
        shared_time.update(game_time)

        # Create gradient background
        game_visuals.create_gradient_background(screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # Volta ao menu ao apertar ESC
            
            if event.type == pygame.KEYDOWN and event.key in input_keys:
                key_label[event.key] = game_time
                # Activate button visual effect
                if event.key in key_to_position:
                    game_visuals.press_button(key_to_position[event.key])

            if event.type == pygame.KEYUP and event.key in input_keys:
                input_start_time = key_label.pop(event.key, None)
                # Deactivate button visual effect
                if event.key in key_to_position:
                    game_visuals.release_button(key_to_position[event.key])

                if input_start_time is not None:
                    input_end_time = game_time
                    input_data.put((event.key, input_start_time, input_end_time))

        if game_time >= music_delay and not music_playing:
            music.music_controller(music_status)
            music_playing = True

        spawn_notes(game_time, tolerance)
        draw_notes(delta_time)
        draw_stylized_hitbox()
        game_visuals.draw_hitbox_buttons(screen, game_time)

        if (game_time > last_note + margin_end and not screen_notes and not pygame.mixer.music.get_busy()):
            return 'score'

        pygame.display.flip()

#Screen Handle
def main():
    #Screen Label
    screens_label = {
        'menu' : interface.menu.menu_screen,
        'select_music' : interface.music_select.select_screen,
        'settings' : interface.settings.settings_screen,
        'score' : interface.game_score.score_screen,
    }

    current_screen = 'menu'
    selected_music = None

    while True:
        if current_screen == 'menu':
            current_screen = screens_label[current_screen](screen, screen_width, screen_height)

        elif current_screen == 'select_music':
            current_screen, selected_music = screens_label[current_screen](screen, screen_width, screen_height)

        elif current_screen == 'settings':
            current_screen = screens_label[current_screen](screen, screen_width, screen_height)

        elif current_screen == 'score':
            current_screen = screens_label[current_screen](screen, screen_width, screen_height, collision_info)

        elif current_screen == 'game':
            current_screen = game_loop(selected_music)

        elif current_screen == 'exit':
            pygame.quit()
            exit()

if __name__ == "__main__":
    main()