import pygame
import sys
import random

pygame.init()

# =====================
# EKRAN
# =====================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cas 5 - Sudar i Game Over")

# =====================
# BOJE
# =====================
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
RED = (220, 0, 0)
BLACK = (0, 0, 0)

# =====================
# SAT
# =====================
clock = pygame.time.Clock()

# =====================
# FONT
# =====================
font = pygame.font.SysFont(None, 50)

# =====================
# IGRAC
# =====================
player_size = 50
player_speed = 5
player_x = WIDTH // 2
player_y = HEIGHT // 2

player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

# =====================
# PREPREKA
# =====================
obstacle_width = 120
obstacle_height = 40
obstacle_x = random.randint(0, WIDTH - obstacle_width)
obstacle_y = random.randint(0, HEIGHT - obstacle_height)

obstacle_rect = pygame.Rect(
    obstacle_x,
    obstacle_y,
    obstacle_width,
    obstacle_height
)

# =====================
# STANJE IGRE
# =====================
game_over = False

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
            # RESTART IGRE
            if game_over and event.key == pygame.K_r:
                player_x = WIDTH // 2
                player_y = HEIGHT // 2
                player_rect.topleft = (player_x, player_y)

                obstacle_rect.x = random.randint(0, WIDTH - obstacle_width)
                obstacle_rect.y = random.randint(0, HEIGHT - obstacle_height)

                game_over = False

    if not game_over:
        # -----------------
        # KRETANJE
        # -----------------
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed

        # -----------------
        # GRANICE
        # -----------------
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > WIDTH:
            player_rect.right = WIDTH
        if player_rect.top < 0:
            player_rect.top = 0
        if player_rect.bottom > HEIGHT:
            player_rect.bottom = HEIGHT

        # -----------------
        # SUDAR
        # -----------------
        if player_rect.colliderect(obstacle_rect):
            game_over = True

    # -----------------
    # CRTANJE
    # -----------------
    screen.fill(WHITE)

    pygame.draw.rect(screen, BLUE, player_rect)
    pygame.draw.rect(screen, RED, obstacle_rect)

    if  game_over:
        text = font.render("GAME OVER", True, BLACK)
        restart_text = font.render("Pritisni R za restart", True, BLACK)

        screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60)
        )
        screen.blit(
            restart_text,
            (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2)
        )

    pygame.display.update()

# =====================
# KRAJ
# =====================
pygame.quit()
sys.exit()
