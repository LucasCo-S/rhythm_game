import pygame
import collision
import queue

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

def draw_modern_card(surface, x, y, width, height, color, alpha=40):
    """Draws a modern, minimalist card with subtle backgrounds"""
    # Main card background - very subtle
    card_rect = pygame.Rect(x, y, width, height)
    card_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(card_surface, (255, 255, 255, 8), card_surface.get_rect(), border_radius=16)
    surface.blit(card_surface, (x, y))
    
    # Subtle colored accent on left side
    accent_rect = pygame.Rect(x, y, 4, height)
    pygame.draw.rect(surface, color, accent_rect, border_radius=2)
    
    # Optional subtle glow
    if alpha > 0:
        glow_surface = pygame.Surface((width + 20, height + 20), pygame.SRCALPHA)
        glow_rect = glow_surface.get_rect()
        pygame.draw.rect(glow_surface, (*color, alpha//4), glow_rect, border_radius=20)
        surface.blit(glow_surface, (x - 10, y - 10))
    
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

def draw_score_highlight(surface, x, y, width, height, score):
    """Draws a modern score highlight section"""
    # Subtle background
    bg_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(bg_surface, (255, 255, 255, 12), bg_surface.get_rect(), border_radius=20)
    surface.blit(bg_surface, (x, y))
    
    # Accent gradient on top
    accent_height = 3
    accent_surface = pygame.Surface((width, accent_height), pygame.SRCALPHA)
    for i in range(width):
        ratio = i / width
        r = int(100 + (255 - 100) * ratio)
        g = int(150 + (220 - 150) * ratio)
        b = int(255)
        pygame.draw.line(accent_surface, (r, g, b, 120), (i, 0), (i, accent_height))
    surface.blit(accent_surface, (x, y))

def score_screen(screen, screen_width, screen_height, collision_info: queue.Queue):
    pygame.font.init()
    
    # Modern font setup
    try:
        font = pygame.font.Font(None, 32)
        title_font = pygame.font.Font(None, 64)
        stat_font = pygame.font.Font(None, 28)
        value_font = pygame.font.Font(None, 44)
        small_font = pygame.font.Font(None, 24)
    except:
        font = pygame.font.SysFont('arial', 32)
        title_font = pygame.font.SysFont('arial', 64, bold=True)
        stat_font = pygame.font.SysFont('arial', 28)
        value_font = pygame.font.SysFont('arial', 44, bold=True)
        small_font = pygame.font.SysFont('arial', 24)

    # Contagem de acertos por tipo
    stats = {
        "PERFECT": 0,
        "GREAT": 0,
        "GOOD": 0,
        "BAD": 0,
        "MISS": 0
    }

    total_hits = 0
    score = 0

    # Processar todos os dados da fila
    while not collision_info.empty():
        hit: collision.Collision_Record = collision_info.get()
        precision = hit.precision.upper()
        stats[precision] += 1
        total_hits += 1
        score += hit.points

    # Calcular precisão percentual
    if total_hits > 0:
        total_possible = total_hits * 500  # 500 é o valor máximo por acerto (PERFECT)
        accuracy = (score / total_possible) * 100
    else:
        accuracy = 0

    # Cores modernas para cada tipo de acerto
    stat_colors = {
        "PERFECT": (255, 195, 50),    # Dourado moderno
        "GREAT": (80, 220, 100),      # Verde vibrante
        "GOOD": (90, 150, 255),       # Azul moderno
        "BAD": (255, 140, 60),        # Laranja suave
        "MISS": (255, 90, 100)        # Vermelho suave
    }

    mouse_pos = (0, 0)
    clock = pygame.time.Clock()

    while True:
        # Criar fundo moderno
        create_modern_background(screen, screen_width, screen_height)

        # Título principal - mais sutil
        title_text = "PERFORMANCE"
        title_surface = title_font.render(title_text, True, (220, 230, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, 70))
        screen.blit(title_surface, title_rect)

        # Seção de pontuação principal
        score_section_width = 400
        score_section_height = 100
        score_section_x = screen_width // 2 - score_section_width // 2
        score_section_y = 120
        
        draw_score_highlight(screen, score_section_x, score_section_y, 
                           score_section_width, score_section_height, score)
        
        # Pontuação
        score_text = f"{score:,}"
        score_surface = value_font.render(score_text, True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen_width // 2, score_section_y + 35))
        screen.blit(score_surface, score_rect)
        
        # Label da pontuação
        score_label = small_font.render("SCORE", True, (150, 160, 200))
        score_label_rect = score_label.get_rect(center=(screen_width // 2, score_section_y + 15))
        screen.blit(score_label, score_label_rect)

        # Precisão
        accuracy_text = f"{accuracy:.1f}% ACCURACY"
        accuracy_surface = stat_font.render(accuracy_text, True, (120, 200, 255))
        accuracy_rect = accuracy_surface.get_rect(center=(screen_width // 2, score_section_y + 65))
        screen.blit(accuracy_surface, accuracy_rect)

        # Cards das estatísticas - layout mais moderno
        card_width = 160
        card_height = 70
        start_y = 260
        spacing = 20
        
        # Calcular posição para centralizar as 5 cards
        total_width = 3 * card_width + 2 * spacing  # Primeira linha: 3 cards
        start_x_top = screen_width // 2 - total_width // 2
        
        # Segunda linha: 2 cards centralizadas
        total_width_bottom = 2 * card_width + spacing
        start_x_bottom = screen_width // 2 - total_width_bottom // 2

        stat_items = list(stats.items())
        
        for i, (stat_name, count) in enumerate(stat_items):
            color = stat_colors[stat_name]
            
            if i < 3:  # Primeira linha
                x = start_x_top + i * (card_width + spacing)
                y = start_y
            else:  # Segunda linha
                x = start_x_bottom + (i - 3) * (card_width + spacing)
                y = start_y + card_height + 25
            
            # Card mais sutil
            draw_modern_card(screen, x, y, card_width, card_height, color, alpha=20)
            
            # Nome da estatística
            name_surface = small_font.render(stat_name, True, color)
            name_rect = name_surface.get_rect(center=(x + card_width // 2, y + 20))
            screen.blit(name_surface, name_rect)
            
            # Valor da estatística
            value_surface = value_font.render(str(count), True, (255, 255, 255))
            value_rect = value_surface.get_rect(center=(x + card_width // 2, y + 45))
            screen.blit(value_surface, value_rect)

        # Botão moderno
        button_width = 280
        button_height = 45
        button_x = screen_width // 2 - button_width // 2
        button_y = screen_height - 100
        
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        is_hovered = button_rect.collidepoint(mouse_pos)
        
        back_button_rect = draw_modern_button(screen, button_x, button_y, button_width, button_height,
                                            "BACK TO SELECTION", font, is_hovered)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "select_music"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button_rect.collidepoint(event.pos):
                    return "select_music"