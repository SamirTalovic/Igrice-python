import pygame
import sys

pygame.init()

# =====================
# EKRAN
# =====================
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cas 12 - Skakanje i gravitacija")

clock = pygame.time.Clock()

# =====================
# BOJE
# =====================
WHITE = (255,255,255)
BLUE = (0,120,255)
GREEN = (0,180,0)
BLACK = (0,0,0)

# =====================
# IGRAC
# =====================
player_rect = pygame.Rect(100, 300, 40, 50)

player_speed = 5
velocity_y = 0

gravity = 0.5
jump_strength = -10

on_ground = False

# =====================
# PLATFORME
# =====================
ground = pygame.Rect(0, 550, 800, 50)

platforms = [
    pygame.Rect(200, 450, 150, 20),
    pygame.Rect(450, 350, 150, 20),
    pygame.Rect(100, 250, 120, 20)
]

# =====================
# GAME LOOP
# =====================
running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # SKOK
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                velocity_y = jump_strength

    # =====================
    # KRETANJE LEVO/DESNO
    # =====================
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed

    # =====================
    # GRAVITACIJA
    # =====================
    velocity_y += gravity
    player_rect.y += velocity_y

    on_ground = False

    # =====================
    # SUDAR SA PODOM
    # =====================
    if player_rect.colliderect(ground):
        player_rect.bottom = ground.top
        velocity_y = 0
        on_ground = True

    # =====================
    # SUDAR SA PLATFORMAMA
    # =====================
    for plat in platforms:
        if player_rect.colliderect(plat) and velocity_y > 0:
            player_rect.bottom = plat.top
            velocity_y = 0
            on_ground = True

    # =====================
    # CRTANJE
    # =====================
    screen.fill(WHITE)

    pygame.draw.rect(screen, BLUE, player_rect)
    pygame.draw.rect(screen, GREEN, ground)

    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)

    pygame.display.update()

pygame.quit()
sys.exit()
