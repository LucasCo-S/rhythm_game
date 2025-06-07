# Importa a biblioteca Pygame, que fornece funcionalidades para criar jogos
import pygame
# Importa todas as constantes do Pygame que nos ajudam a detectar:
# - Teclas pressionadas (K_UP, K_DOWN, K_LEFT, K_RIGHT, etc)
# - Cliques do mouse (MOUSEBUTTONDOWN, MOUSEBUTTONUP)
# - Movimento do mouse (MOUSEMOTION)
# - Eventos da janela (QUIT, VIDEORESIZE)
# - Eventos do sistema (KEYDOWN, KEYUP)
from pygame.locals import *

# Importa a função exit() do módulo sys para encerrar o programa de forma limpa
from sys import exit

from random import randint

pygame.init()

screen_width: int = 1280

screen_height: int = 720

screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

x = int(screen_width / 2)

y = int(screen_height / 2)

x_blue = x

y_blue = y

while True:
    clock.tick(30)

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()

    if keys[K_a] and x > 0:
        x -= 10
    if keys[K_d] and x < screen_width - 40:
        x += 10
    if keys[K_w] and y > 0:
        y -= 10
    if keys[K_s] and y < screen_height - 50:
        y += 10

    rect1 = pygame.draw.rect(screen, (255,0,0), (x, y, 40,50))

    rect2 = pygame.draw.rect(screen, (0,0,255), (x_blue, y_blue, 40,50))

    if rect1 == rect2:
        print("Colidiram perfeitamente")

    if rect1.colliderect(rect2):
       print("Se encostaram")


    pygame.display.flip()
