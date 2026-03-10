import pygame
import sys
import random

pygame.init()

# =====================
# EKRAN
# =====================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cas 7 - Zivoti i Meni")

# =====================
# BOJE
# =====================
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
RED = (220, 0, 0)
BLACK = (0, 0, 0)

# =====================
# FONT
# =====================
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

# =====================
# SAT
# =====================
clock = pygame.time.Clock()

# =====================
# IGRAC
# =====================
player_size = 40
player_speed = 5
player_rect = pygame.Rect(
    WIDTH // 2, HEIGHT // 2, player_size, player_size
)

# =====================
# PREPREKE
# =====================
obstacles = []

def create_obstacles():
    obstacles.clear()
    for _ in range(5):
        rect = pygame.Rect(
            random.randint(0, WIDTH - 100),
            random.randint(0, HEIGHT - 40),
            100,
            40
        )
        speed = random.randint(2, 4)
        direction = random.choice([-1, 1])
        obstacles.append([rect, speed, direction])

create_obstacles()

# =====================
# IGRA
# =====================
lives = 3
score = 0
score_timer = 0

game_state = "menu"  # menu, play, gameover

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
            if game_state == "menu" and event.key == pygame.K_SPACE:
                game_state = "play"
                lives = 3
                score = 0
                player_rect.center = (WIDTH // 2, HEIGHT // 2)
                create_obstacles()

            if game_state == "gameover" and event.key == pygame.K_r:
                game_state = "menu"

    # =====================
    # PLAY STATE
    # =====================
    if game_state == "play":
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
        player_rect.clamp_ip(screen.get_rect())

        # PREPREKE SE KRECU
        for obs in obstacles:
            obs[0].y += obs[1] * obs[2]
            if obs[0].top <= 0 or obs[0].bottom >= HEIGHT:
                obs[2] *= -1

        # POENI
        score_timer += 1
        if score_timer >= 60:
            score += 1
            score_timer = 0

        # SUDAR
        for obs in obstacles:
            if player_rect.colliderect(obs[0]):
                lives -= 1
                player_rect.center = (WIDTH // 2, HEIGHT // 2)
                pygame.time.delay(400)
                if lives <= 0:
                    game_state = "gameover"

    # =====================
    # CRTANJE
    # =====================
    screen.fill(WHITE)

    if game_state == "menu":
        title = big_font.render("MOJA IGRICA", True, BLACK)
        info = font.render("Pritisni SPACE za start", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
        screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 280))

    elif game_state == "play":
        pygame.draw.rect(screen, BLUE, player_rect)
        for obs in obstacles:
            pygame.draw.rect(screen, RED, obs[0])

        lives_text = font.render(f"Zivoti: {lives}", True, BLACK)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(lives_text, (10, 10))
        screen.blit(score_text, (10, 50))

    elif game_state == "gameover":
        over = big_font.render("GAME OVER", True, BLACK)
        restart = font.render("Pritisni R za meni", True, BLACK)
        screen.blit(over, (WIDTH // 2 - over.get_width() // 2, 220))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 300))

    pygame.display.update()

pygame.quit()
sys.exit()
