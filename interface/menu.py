import pygame
from interface.game_score import create_modern_background, draw_modern_button

def menu_screen(screen: pygame.Surface, screen_width: int, screen_height: int):
    pygame.font.init()

    try:
        title_font = pygame.font.Font(None, 72)
        button_font = pygame.font.Font(None, 40)
    except:
        title_font = pygame.font.SysFont('arial', 72)
        button_font = pygame.font.SysFont('arial', 40)

    clock = pygame.time.Clock()

    button_width = 280
    button_height = 50
    spacing = 30

    buttons = [
        {"label": "INICIAR", "action": "select_music"},
        {"label": "CONFIGURAÇÕES", "action": "settings"},
        {"label": "SAIR", "action": "exit"},
    ]

    while True:
        create_modern_background(screen, screen_width, screen_height)

        # Título centralizado
        title = title_font.render("Rhyphos", True, (240, 240, 255))
        title_rect = title.get_rect(center=(screen_width // 2, 120))
        screen.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        for i, button in enumerate(buttons):
            x = screen_width // 2 - button_width // 2
            y = 250 + i * (button_height + spacing)

            hovered = pygame.Rect(x, y, button_width, button_height).collidepoint(mouse_pos)

            button_rect = draw_modern_button(
                screen, x, y, button_width, button_height,
                button["label"], button_font, is_hovered=hovered
            )

            button["rect"] = button_rect  # Salva para detecção de clique

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        return button["action"]
