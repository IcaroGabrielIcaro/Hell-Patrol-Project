import pygame
import socket
import json

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5555))

running = True

while running:
    dx, dy = 0, 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: dy = -1
    if keys[pygame.K_s]: dy = 1
    if keys[pygame.K_a]: dx = -1
    if keys[pygame.K_d]: dx = 1

    msg = {
        "action": "move",
        "dx": dx,
        "dy": dy
    }

    client.sendall(json.dumps(msg).encode())

    data = client.recv(4096).decode()
    state = json.loads(data)

    screen.fill((30, 30, 30))

    for player in state["players"].values():
        pygame.draw.rect(
            screen,
            (200, 50, 50),
            (player["x"], player["y"], 40, 40)
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
client.close()
