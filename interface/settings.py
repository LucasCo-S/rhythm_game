import pygame
import json
import os

settings_path = "settings/user.json"

def load_settings() -> dict:
    if not os.path.exists(settings_path):
        return {
            "volume": 1.0,
            "keys": {
                "1": "a",
                "2": "s",
                "3": "k",
                "4": "l"
            },
        }
    with open(settings_path, "r", encoding="utf-8") as file:
        return json.load(file)

def save_settings(settings: dict):
    with open(settings_path, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)

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

def draw_modern_card(surface, x, y, width, height, accent_color=(100, 180, 255)):
    """Draws a modern, minimalist card"""
    card_rect = pygame.Rect(x, y, width, height)
    
    # Main card background - very subtle
    card_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(card_surface, (255, 255, 255, 12), card_surface.get_rect(), border_radius=16)
    surface.blit(card_surface, (x, y))
    
    # Subtle colored accent on left side
    accent_rect = pygame.Rect(x, y, 4, height)
    pygame.draw.rect(surface, accent_color, accent_rect, border_radius=2)
    
    return card_rect

def draw_modern_button(surface, x, y, width, height, text, font, is_hovered=False, style="normal"):
    """Draws a modern, flat button with hover effects"""
    button_rect = pygame.Rect(x, y, width, height)
    
    if style == "volume":
        # Volume control buttons
        if is_hovered:
            bg_color = (70, 85, 140, 180)
            text_color = (255, 255, 255)
            border_color = (100, 180, 255)
        else:
            bg_color = (255, 255, 255, 20)
            text_color = (180, 190, 220)
            border_color = (60, 70, 90)
        
        bg_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, bg_color, bg_surface.get_rect(), border_radius=8)
        surface.blit(bg_surface, (x, y))
        
        # Subtle border
        pygame.draw.rect(surface, border_color, button_rect, width=1, border_radius=8)
        
    elif style == "key":
        # Key binding buttons
        if is_hovered:
            bg_color = (70, 130, 180, 100)
            text_color = (255, 255, 255)
            glow_surface = pygame.Surface((width + 10, height + 10), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (70, 130, 180, 30), glow_surface.get_rect(), border_radius=18)
            surface.blit(glow_surface, (x - 5, y - 5))
        else:
            bg_color = (255, 255, 255, 15)
            text_color = (200, 210, 230)
        
        bg_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, bg_color, bg_surface.get_rect(), border_radius=12)
        surface.blit(bg_surface, (x, y))
        
    else:
        # Normal buttons
        if is_hovered:
            bg_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(bg_surface, (70, 85, 140, 180), bg_surface.get_rect(), border_radius=12)
            
            # Subtle glow effect
            glow_surface = pygame.Surface((width + 20, height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (70, 85, 140, 30), glow_surface.get_rect(), border_radius=16)
            surface.blit(glow_surface, (x - 10, y - 10))
            
            surface.blit(bg_surface, (x, y))
            text_color = (255, 255, 255)
        else:
            bg_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(bg_surface, (255, 255, 255, 15), bg_surface.get_rect(), border_radius=12)
            surface.blit(bg_surface, (x, y))
            text_color = (180, 190, 220)
    
    # Draw button text
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)
    
    return button_rect

def draw_volume_slider(surface, x, y, width, height, volume, font):
    """Draws a modern volume slider"""
    # Background track
    track_height = 6
    track_y = y + (height - track_height) // 2
    track_rect = pygame.Rect(x, track_y, width, track_height)
    
    # Track background
    track_surface = pygame.Surface((width, track_height), pygame.SRCALPHA)
    pygame.draw.rect(track_surface, (255, 255, 255, 30), track_surface.get_rect(), border_radius=3)
    surface.blit(track_surface, (x, track_y))
    
    # Filled track
    fill_width = int(width * volume)
    if fill_width > 0:
        fill_surface = pygame.Surface((fill_width, track_height), pygame.SRCALPHA)
        pygame.draw.rect(fill_surface, (100, 180, 255, 200), fill_surface.get_rect(), border_radius=3)
        surface.blit(fill_surface, (x, track_y))
    
    # Volume handle
    handle_x = x + fill_width - 8
    handle_rect = pygame.Rect(handle_x, y + height//2 - 10, 16, 20)
    pygame.draw.rect(surface, (255, 255, 255), handle_rect, border_radius=8)
    pygame.draw.rect(surface, (100, 180, 255), handle_rect, width=2, border_radius=8)

def settings_screen(screen: pygame.Surface, screen_width: int, screen_height: int) -> str:
    pygame.font.init()
    
    # Modern font setup
    try:
        title_font = pygame.font.Font(None, 52)
        section_font = pygame.font.Font(None, 32)
        font = pygame.font.Font(None, 28)
        small_font = pygame.font.Font(None, 24)
    except:
        title_font = pygame.font.SysFont('arial', 52, bold=True)
        section_font = pygame.font.SysFont('arial', 32)
        font = pygame.font.SysFont('arial', 28)
        small_font = pygame.font.SysFont('arial', 24)

    settings = load_settings()
    volume = settings["volume"]

    # Modern layout
    card_width = 600
    volume_card_height = 120
    keys_card_height = 280
    
    volume_card_x = (screen_width - card_width) // 2
    volume_card_y = 150
    
    keys_card_x = volume_card_x
    keys_card_y = volume_card_y + volume_card_height + 30

    # Volume controls
    increase_volume_rect = pygame.Rect(volume_card_x + card_width - 140, volume_card_y + 65, 40, 40)
    decrease_volume_rect = pygame.Rect(volume_card_x + card_width - 190, volume_card_y + 65, 40, 40)
    
    # Volume slider area
    slider_x = volume_card_x + 30
    slider_y = volume_card_y + 70
    slider_width = card_width - 280
    slider_height = 30

    # Key binding rectangles
    keys_rects = {}
    key_button_width = card_width - 60
    key_button_height = 45
    start_y = keys_card_y + 50
    
    for i, (key, actual_key) in enumerate(settings["keys"].items()):
        rect = pygame.Rect(keys_card_x + 30, start_y + i * 55, key_button_width, key_button_height)
        keys_rects[key] = (rect, actual_key)

    # Return button
    return_button_width = 140
    return_button_height = 45
    return_rect = pygame.Rect(50, screen_height - 80, return_button_width, return_button_height)

    change_key = None
    clock = pygame.time.Clock()
    mouse_pos = (0, 0)

    while True:
        # Create modern background
        create_modern_background(screen, screen_width, screen_height)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Modern title
        title_text = "SETTINGS"
        title_surface = title_font.render(title_text, True, (220, 230, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, 70))
        screen.blit(title_surface, title_rect)

        # Volume Card
        draw_modern_card(screen, volume_card_x, volume_card_y, card_width, volume_card_height, (255, 140, 60))
        
        # Volume section title
        vol_title = section_font.render("AUDIO", True, (255, 140, 60))
        screen.blit(vol_title, (volume_card_x + 30, volume_card_y + 20))
        
        # Volume display
        vol_txt = font.render(f"Volume: {volume:.1f}", True, (255, 255, 255))
        screen.blit(vol_txt, (volume_card_x + 30, volume_card_y + 50))
        
        # Volume slider
        draw_volume_slider(screen, slider_x, slider_y, slider_width, slider_height, volume, font)
        
        # Volume control buttons
        decrease_hovered = decrease_volume_rect.collidepoint(mouse_pos)
        increase_hovered = increase_volume_rect.collidepoint(mouse_pos)
        
        draw_modern_button(screen, decrease_volume_rect.x, decrease_volume_rect.y, 
                          decrease_volume_rect.width, decrease_volume_rect.height,
                          "−", font, decrease_hovered, "volume")
        
        draw_modern_button(screen, increase_volume_rect.x, increase_volume_rect.y,
                          increase_volume_rect.width, increase_volume_rect.height,
                          "+", font, increase_hovered, "volume")

        # Key Bindings Card
        draw_modern_card(screen, keys_card_x, keys_card_y, card_width, keys_card_height, (100, 180, 255))
        
        # Key bindings section title
        keys_title = section_font.render("KEY BINDINGS", True, (100, 180, 255))
        screen.blit(keys_title, (keys_card_x + 30, keys_card_y + 20))
        
        # Key binding buttons
        for key_name, (rect, key) in keys_rects.items():
            is_hovered = rect.collidepoint(mouse_pos)
            is_changing = change_key == key_name
            
            if is_changing:
                # Special highlight for key being changed
                glow_surface = pygame.Surface((rect.width + 10, rect.height + 10), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (255, 195, 50, 60), glow_surface.get_rect(), border_radius=18)
                screen.blit(glow_surface, (rect.x - 5, rect.y - 5))
                
                bg_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                pygame.draw.rect(bg_surface, (255, 195, 50, 80), bg_surface.get_rect(), border_radius=12)
                screen.blit(bg_surface, rect)
                text_color = (255, 255, 255)
            else:
                draw_modern_button(screen, rect.x, rect.y, rect.width, rect.height, "", font, is_hovered, "key")
                text_color = (255, 255, 255) if is_hovered else (200, 210, 230)
            
            # Key binding text
            if is_changing:
                msg_text = f"{key_name.upper()}: Press a key..."
            else:
                msg_text = f"{key_name.upper()}: {key.upper()}"
            
            msg = font.render(msg_text, True, text_color)
            msg_rect = msg.get_rect(center=rect.center)
            screen.blit(msg, msg_rect)

        # Return Button
        is_return_hovered = return_rect.collidepoint(mouse_pos)
        draw_modern_button(screen, return_rect.x, return_rect.y, return_rect.width, return_rect.height,
                          "← BACK", font, is_return_hovered)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                save_settings(settings)
                return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if return_rect.collidepoint(event.pos):
                    save_settings(settings)
                    return "menu"

                if increase_volume_rect.collidepoint(event.pos):
                    volume = min(1.0, volume + 0.1)
                    settings["volume"] = round(volume, 1)

                if decrease_volume_rect.collidepoint(event.pos):
                    volume = max(0.0, volume - 0.1)
                    settings["volume"] = round(volume, 1)

                for key_name, (rect, _) in keys_rects.items():
                    if rect.collidepoint(event.pos):
                        change_key = key_name

            if event.type == pygame.KEYDOWN and change_key:
                new_key = pygame.key.name(event.key)
                settings["keys"][change_key] = new_key
                keys_rects[change_key] = (keys_rects[change_key][0], new_key)
                change_key = None