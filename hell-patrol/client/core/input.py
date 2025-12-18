import pygame

def get_movement():
    dx, dy = 0, 0
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]: dy = -1
    if keys[pygame.K_s]: dy = 1
    if keys[pygame.K_a]: dx = -1
    if keys[pygame.K_d]: dx = 1

    return dx, dy
