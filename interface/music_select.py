import pygame
from typing import List
import os

def create_modern_background(surface, screen_width, screen_height):
    """Creates a modern dark background with subtle gradients"""
    # Base dark background
    surface.fill((12, 15, 22))
    
    # Subtle gradient overlay
    gradient_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    for y in range(screen_height):
        ratio = y / screen_height
        alpha = int(15 * (1 - ratio))
        color = (25, 30, 45, alpha)
        pygame.draw.line(gradient_surface, color, (0, y), (screen_width, y))
    surface.blit(gradient_surface, (0, 0))

def draw_modern_card(surface, x, y, width, height, is_hovered=False):
    """Draws a modern, minimalist card for music selection"""
    card_rect = pygame.Rect(x, y, width, height)
    
    if is_hovered:
        # Hover state - subtle glow and brighter background
        glow_surface = pygame.Surface((width + 10, height + 10), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (70, 85, 140, 40), glow_surface.get_rect(), border_radius=18)
        surface.blit(glow_surface, (x - 5, y - 5))
        
        card_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(card_surface, (255, 255, 255, 25), card_surface.get_rect(), border_radius=16)
        surface.blit(card_surface, (x, y))
        
        # Colored accent on left side
        accent_rect = pygame.Rect(x, y, 4, height)
        pygame.draw.rect(surface, (100, 180, 255), accent_rect, border_radius=2)
    else:
        # Normal state - very subtle background
        card_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(card_surface, (255, 255, 255, 8), card_surface.get_rect(), border_radius=16)
        surface.blit(card_surface, (x, y))
        
        # Subtle accent on left side
        accent_rect = pygame.Rect(x, y, 2, height)
        pygame.draw.rect(surface, (60, 70, 90), accent_rect, border_radius=1)
    
    return card_rect

def draw_modern_button(surface, x, y, width, height, text, font, is_hovered=False):
    """Draws a modern, flat button with hover effects"""
    button_rect = pygame.Rect(x, y, width, height)
    
    if is_hovered:
        # Hover state - slightly brighter with subtle glow
        bg_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (70, 85, 140, 180), bg_surface.get_rect(), border_radius=12)
        
        # Subtle glow effect
        glow_surface = pygame.Surface((width + 20, height + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (70, 85, 140, 30), glow_surface.get_rect(), border_radius=16)
        surface.blit(glow_surface, (x - 10, y - 10))
        
        surface.blit(bg_surface, (x, y))
        text_color = (255, 255, 255)
    else:
        # Normal state - very subtle background
        bg_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (255, 255, 255, 15), bg_surface.get_rect(), border_radius=12)
        surface.blit(bg_surface, (x, y))
        text_color = (180, 190, 220)
    
    # Draw button text
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)
    
    return button_rect

def select_screen(screen: pygame.Surface, screen_width: int, screen_height: int):
    pygame.font.init()
    
    # Modern font setup
    try:
        title_font = pygame.font.Font(None, 52)
        music_font = pygame.font.Font(None, 32)
        button_font = pygame.font.Font(None, 28)
    except:
        title_font = pygame.font.SysFont('arial', 52, bold=True)
        music_font = pygame.font.SysFont('arial', 32)
        button_font = pygame.font.SysFont('arial', 28)

    musics: List[str] = music_list()

    # Define selection buttons particulars - more modern spacing
    button_width = 500
    button_height = 60
    padding = 15
    top_offset = 150

    buttons = []
    for i, music in enumerate(musics):
        x = (screen_width - button_width) // 2
        y = top_offset + i * (button_height + padding)
        rect = pygame.Rect(x, y, button_width, button_height)
        buttons.append((music, rect))

    # Return button - more modern positioning
    return_button_width = 140
    return_button_height = 45
    return_rect = pygame.Rect(50, screen_height - 80, return_button_width, return_button_height)

    clock = pygame.time.Clock()
    mouse_pos = (0, 0)

    while True:
        # Create modern background
        create_modern_background(screen, screen_width, screen_height)
        
        # Modern title
        title_text = "MUSIC SELECTION"
        title_surface = title_font.render(title_text, True, (220, 230, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, 70))
        screen.blit(title_surface, title_rect)
        
        # Subtitle with gradient effect
        subtitle_text = "Choose your track"
        subtitle_surface = music_font.render(subtitle_text, True, (150, 160, 200))
        subtitle_rect = subtitle_surface.get_rect(center=(screen_width // 2, 110))
        screen.blit(subtitle_surface, subtitle_rect)

        # Music Selection Cards
        mouse_pos = pygame.mouse.get_pos()
        
        for music, rect in buttons:
            is_hovered = rect.collidepoint(mouse_pos)
            draw_modern_card(screen, rect.x, rect.y, rect.width, rect.height, is_hovered)
            
            # Music name with better typography
            text_color = (255, 255, 255) if is_hovered else (200, 210, 230)
            music_text = music_font.render(music, True, text_color)
            text_rect = music_text.get_rect(center=rect.center)
            screen.blit(music_text, text_rect)
            
            # Add subtle play icon or indicator
            if is_hovered:
                play_icon = music_font.render("►", True, (100, 180, 255))
                play_rect = play_icon.get_rect(center=(rect.x + 30, rect.centery))
                screen.blit(play_icon, play_rect)

        # Modern Return Button
        is_return_hovered = return_rect.collidepoint(mouse_pos)
        draw_modern_button(screen, return_rect.x, return_rect.y, return_rect.width, return_rect.height,
                          "← BACK", button_font, is_return_hovered)

        # Display Update
        pygame.display.flip()
        clock.tick(60)

        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return ("menu", None)
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if return_rect.collidepoint(event.pos):
                    return ("menu", None)
                
                for music, rect in buttons:
                    if rect.collidepoint(event.pos):
                        return ("game", music)

def music_list() -> List[str]:
    mapped_music_path: str = "mapped_music/"

    musics: List[str] = []

    for music in os.listdir(mapped_music_path):
        path_music = os.path.join(mapped_music_path, music)

        if os.path.isdir(path_music):
            music_name = music.split("_")[1]
            musics.append(music_name)

    return musics