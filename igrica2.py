import pygame
import sys
import random

pygame.init()

# =====================
# EKRAN
# =====================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cas 4 - Dodaci")

# =====================
# BOJE
# =====================
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
BLACK = (0, 0, 0)

# =====================
# SAT (FPS)
# =====================
clock = pygame.time.Clock()

# =====================
# FONT
# =====================
font = pygame.font.SysFont(None, 60)

# =====================
# IGRAC
# =====================
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT // 2

normal_speed = 5
fast_speed = 9

player_color = BLUE

# =====================
# PAUZA
# =====================
paused = False

# =====================
# GAME LOOP
# =====================
running = True
while running:
    clock.tick(60)

    # -----------------
    # DOGADJAJI
    # -----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # TELEPORT U SREDINU
            if event.key == pygame.K_r and not paused:
                player_x = WIDTH // 2
                player_y = HEIGHT // 2

            # PROMENA BOJE
            if event.key == pygame.K_c:
                player_color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )

            # PAUZA
            if event.key == pygame.K_p:
                paused = not paused

    # -----------------
    # AKO JE PAUZA
    # -----------------
    if paused:
        screen.fill(WHITE)
        pause_text = font.render("PAUZA", True, BLACK)
        screen.blit(
            pause_text,
            (
                WIDTH // 2 - pause_text.get_width() // 2,
                HEIGHT // 2 - pause_text.get_height() // 2
            )
        )
        pygame.display.update()
        continue

    # -----------------
    # DRZANJE TASTERA
    # -----------------
    keys = pygame.key.get_pressed()

    speed = normal_speed
    if keys[pygame.K_LSHIFT]:
        speed = fast_speed

    if keys[pygame.K_LEFT]:
        player_x -= speed
    if keys[pygame.K_RIGHT]:
        player_x += speed
    if keys[pygame.K_UP]:
        player_y -= speed
    if keys[pygame.K_DOWN]:
        player_y += speed

    # -----------------
    # GRANICE EKRANA
    # -----------------
    if player_x < 0:
        player_x = 0
    if player_x > WIDTH - player_size:
        player_x = WIDTH - player_size
    if player_y < 0:
        player_y = 0
    if player_y > HEIGHT - player_size:
        player_y = HEIGHT - player_size

    # -----------------
    # CRTANJE
    # -----------------
    screen.fill(WHITE)

    pygame.draw.rect(
        screen,
        player_color,
        (player_x, player_y, player_size, player_size)
    )

    pygame.display.update()

# =====================
# KRAJ
# =====================
pygame.quit()
sys.exit()
