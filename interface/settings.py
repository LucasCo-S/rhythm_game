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

def settings_screen(screen: pygame.Surface, screen_width: int, screen_height: int) -> str:
    pygame.font.init()
    font = pygame.font.SysFont(None, 36)

    settings = load_settings()
    volume = settings["volume"]

    return_rect = pygame.Rect(40, 600, 150, 40)
    increase_volume_rect = pygame.Rect(40, 180, 50, 40)
    decrease_volume_rect = pygame.Rect(100, 180, 50, 40)

    # Retângulos das teclas
    keys_rects = {}
    pos_y = 260
    for key, actual_key in settings["keys"].items():
        rect = pygame.Rect(40, pos_y, 300, 40)
        keys_rects[key] = (rect, actual_key)
        pos_y += 50

    change_key = None

    while True:
        screen.fill((30, 30, 30))
        
        text_color = (255, 255, 255)

        #Title
        title = font.render("Configurações", False, text_color)
        screen.blit(title, (screen_height // 2 - title.get_width() // 2, 40))

        #Volume
        vol_txt = font.render(f"Volume: {volume:.1f}", True, text_color)
        screen.blit(vol_txt, (40, 150))

        pygame.draw.rect(screen, (80, 80, 80), increase_volume_rect)
        pygame.draw.rect(screen, (80, 80, 80), decrease_volume_rect)

        screen.blit(font.render("+", True, (255, 255, 255)), (increase_volume_rect.x + 10, decrease_volume_rect.y + 5))
        screen.blit(font.render("-", True, (255, 255, 255)), (increase_volume_rect.x + 10, decrease_volume_rect.y + 5))

        #Keybinds
        for key_name, (rect, key) in keys_rects.items():
            color = (70, 130, 180) if change_key == key_name else (70, 70, 70)
            pygame.draw.rect(screen, color, rect)
            msg = font.render(f"{key_name.capitalize()}: {key.upper()}", True, (255, 255, 255))

            screen.blit(msg, (rect.x + 10, rect.y + 5))

        #Return Button
        pygame.draw.rect(screen, (80, 80, 80), return_rect)
        screen.blit(font.render("Voltar", True, (255, 255, 255)), (return_rect.x + 10, return_rect.y + 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

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
