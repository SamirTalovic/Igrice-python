import pygame
import sys
import random

pygame.init()

# =====================
# EKRAN
# =====================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cas 8 - Leveli i Sakupljanje")

# =====================
# BOJE
# =====================
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLACK = (0, 0, 0)

# =====================
# FONT
# =====================
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 60)

clock = pygame.time.Clock()

# =====================
# IGRAC
# =====================
player_size = 40
player_speed = 5
player_rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, player_size, player_size)

# =====================
# COLLECT ITEM
# =====================
item_size = 25
item_rect = pygame.Rect(
    random.randint(0, WIDTH - item_size),
    random.randint(0, HEIGHT - item_size),
    item_size,
    item_size
)

# =====================
# PREPREKE
# =====================
obstacles = []

def create_obstacles(level):
    obstacles.clear()
    for _ in range(level + 1):
        rect = pygame.Rect(
            random.randint(0, WIDTH - 100),
            random.randint(0, HEIGHT - 40),
            100,
            40
        )
        speed = random.randint(2, 3 + level)
        direction = random.choice([-1, 1])
        obstacles.append([rect, speed, direction])

# =====================
# IGRA
# =====================
level = 1
score = 0
lives = 3

game_state = "play"  # odmah u igru

create_obstacles(level)

# =====================
# GAME LOOP
# =====================
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "play":
        # KRETANJE
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed

        player_rect.clamp_ip(screen.get_rect())

        # PREPREKE
        for obs in obstacles:
            obs[0].y += obs[1] * obs[2]
            if obs[0].top <= 0 or obs[0].bottom >= HEIGHT:
                obs[2] *= -1

            if player_rect.colliderect(obs[0]):
                lives -= 1
                player_rect.center = (WIDTH // 2, HEIGHT // 2)
                pygame.time.delay(300)
                if lives <= 0:
                    game_state = "gameover"

        # COLLECT
        if player_rect.colliderect(item_rect):
            score += 1
            item_rect.topleft = (
                random.randint(0, WIDTH - item_size),
                random.randint(0, HEIGHT - item_size)
            )

            if score % 5 == 0:
                level += 1
                create_obstacles(level)

    # =====================
    # CRTANJE
    # =====================
    screen.fill(WHITE)

    if game_state == "play":
        pygame.draw.rect(screen, BLUE, player_rect)
        pygame.draw.rect(screen, GREEN, item_rect)

        for obs in obstacles:
            pygame.draw.rect(screen, RED, obs[0])

        screen.blit(font.render(f"Level: {level}", True, BLACK), (10, 10))
        screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 40))
        screen.blit(font.render(f"Zivoti: {lives}", True, BLACK), (10, 70))

    else:
        over = big_font.render("GAME OVER", True, BLACK)
        screen.blit(over, (WIDTH//2 - over.get_width()//2, 260))

    pygame.display.update()

pygame.quit()
sys.exit()
