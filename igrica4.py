import pygame
import sys
import random

pygame.init()

# =====================
# EKRAN
# =====================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cas 6 - Poeni i Pokretne Prepreke")

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
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

# =====================
# IGRAC
# =====================
player_size = 50
player_speed = 5
player_rect = pygame.Rect(
    WIDTH // 2, HEIGHT // 2, player_size, player_size
)

# =====================
# PREPREKA
# =====================
obstacle_width = 120
obstacle_height = 40
obstacle_rect = pygame.Rect(
    random.randint(0, WIDTH - obstacle_width),
    random.randint(0, HEIGHT - obstacle_height),
    obstacle_width,
    obstacle_height
)

obstacle_speed = 4
obstacle_direction = 1  # 1 = dole, -1 = gore

# =====================
# POENI
# =====================
score = 0
score_timer = 0

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
            # RESTART
            if game_over and event.key == pygame.K_r:
                player_rect.center = (WIDTH // 2, HEIGHT // 2)

                obstacle_rect.x = random.randint(0, WIDTH - obstacle_width)
                obstacle_rect.y = random.randint(0, HEIGHT - obstacle_height)

                obstacle_speed = 4
                score = 0
                score_timer = 0
                game_over = False

    if not game_over:
        # -----------------
        # KRETANJE IGRACA
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

        # GRANICE
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > WIDTH:
            player_rect.right = WIDTH
        if player_rect.top < 0:
            player_rect.top = 0
        if player_rect.bottom > HEIGHT:
            player_rect.bottom = HEIGHT

        # -----------------
        # KRETANJE PREPREKE
        # -----------------
        obstacle_rect.y += obstacle_speed * obstacle_direction

        if obstacle_rect.top <= 0 or obstacle_rect.bottom >= HEIGHT:
            obstacle_direction *= -1

        # -----------------
        # POENI (VREME)
        # -----------------
        score_timer += 1
        if score_timer >= 60:  # svake 1 sekunde
            score += 1
            score_timer = 0

            # povecaj tezinu
            if score % 5 == 0:
                obstacle_speed += 1

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

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if game_over:
        over_text = big_font.render("GAME OVER", True, BLACK)
        restart_text = font.render("Pritisni R za restart", True, BLACK)

        screen.blit(
            over_text,
            (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 60)
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
