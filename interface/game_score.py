import pygame
import interface.music_select  # Para retornar corretamente
import collision
import queue

def score_screen(screen, screen_width, screen_height, collision_info: queue.Queue):
    pygame.font.init()
    font = pygame.font.SysFont(None, 48)
    title_font = pygame.font.SysFont(None, 64)

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

    while True:
        screen.fill((20, 20, 20))

        # Título
        title = title_font.render("Desempenho", True, (255, 255, 255))
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 50))

        # Estatísticas
        stat_texts = [
            f"Pontuação: {score}",
            f"Perfect: {stats['PERFECT']}",
            f"Great: {stats['GREAT']}",
            f"Good: {stats['GOOD']}",
            f"Bad: {stats['BAD']}",
            f"Miss: {stats['MISS']}",
            f"Precisão: {accuracy:.2f}%"
        ]

        for i, text in enumerate(stat_texts):
            rendered = font.render(text, True, (255, 255, 255))
            screen.blit(rendered, (screen_width // 2 - rendered.get_width() // 2, 150 + i * 50))

        # Botão de voltar
        back_text = font.render("Voltar para Seleção de Música", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(screen_width // 2, screen_height - 100))
        pygame.draw.rect(screen, (70, 70, 70), back_rect.inflate(20, 10))
        screen.blit(back_text, back_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(event.pos):
                    return "select_music"
