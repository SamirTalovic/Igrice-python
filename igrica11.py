import pygame
import sys
import random

pygame.init()

# =====================
# EKRAN
# =====================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer - Leveli")

clock = pygame.time.Clock()

# =====================
# BOJE
# =====================
WHITE = (255,255,255)
BLUE = (0,120,255)
GREEN = (0,180,0)
RED = (200,0,0)
YELLOW = (240,200,0)

# =====================
# IGRAC
# =====================
player = pygame.Rect(100, 300, 40, 50)

player_speed = 5
velocity_y = 0

gravity = 0.5
jump_strength = -10

on_ground = False

# =====================
# POD
# =====================
ground = pygame.Rect(0, 550, 800, 50)

# =====================
# LEVEL
# =====================
level = 1

# =====================
# PLATFORME
# =====================
platforms = []
moving_platform = pygame.Rect(300, 250, 150, 20)
platform_speed = 2
platform_direction = 1

# =====================
# NEPRIJATELJ
# =====================
enemy = pygame.Rect(400, 500, 40, 40)
enemy_speed = 3
enemy_direction = 1

# =====================
# GOAL
# =====================
goal = pygame.Rect(700, 500, 40, 50)

# =====================
# FUNKCIJA ZA LEVEL
# =====================
def create_level():
    global platforms, enemy_speed

    platforms = []

    for _ in range(level + 1):
        platforms.append(
            pygame.Rect(
                random.randint(100, 600),
                random.randint(200, 500),
                120,
                20
            )
        )

    enemy.x = random.randint(100, 700)
    enemy.y = 500
    enemy_speed = 2 + level

    goal.x = random.randint(600, 750)
    goal.y = 500

create_level()

# =====================
# GAME LOOP
# =====================
running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                velocity_y = jump_strength

    # =====================
    # KRETANJE IGRACA
    # =====================
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= player_speed

    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # =====================
    # GRAVITACIJA
    # =====================
    velocity_y += gravity
    player.y += velocity_y

    on_ground = False

    # =====================
    # POD
    # =====================
    if player.colliderect(ground):
        player.bottom = ground.top
        velocity_y = 0
        on_ground = True

    # =====================
    # PLATFORME
    # =====================
    for plat in platforms:
        if player.colliderect(plat) and velocity_y > 0:
            player.bottom = plat.top
            velocity_y = 0
            on_ground = True

    # =====================
    # POKRETNA PLATFORMA
    # =====================
    moving_platform.x += platform_speed * platform_direction

    if moving_platform.left <= 0 or moving_platform.right >= WIDTH:
        platform_direction *= -1

    if player.colliderect(moving_platform) and velocity_y > 0:
        player.bottom = moving_platform.top
        velocity_y = 0
        on_ground = True
        player.x += platform_speed * platform_direction

    # =====================
    # ENEMY
    # =====================
    enemy.x += enemy_speed * enemy_direction

    if enemy.left <= 0 or enemy.right >= WIDTH:
        enemy_direction *= -1

    if player.colliderect(enemy):
        print("GAME OVER")
        running = False

    # =====================
    # GOAL (NAJBITNIJE)
    # =====================
    if player.colliderect(goal):
        level += 1
        player.x = 100
        player.y = 300
        create_level()

    # =====================
    # CRTANJE
    # =====================
    screen.fill(WHITE)

    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, GREEN, ground)

    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)

    pygame.draw.rect(screen, GREEN, moving_platform)
    pygame.draw.rect(screen, RED, enemy)

    # GOAL
    pygame.draw.rect(screen, YELLOW, goal)

    # LEVEL TEXT
    font = pygame.font.SysFont(None, 36)
    level_text = font.render(f"Level: {level}", True, (0,0,0))
    screen.blit(level_text, (10, 10))

    pygame.display.update()

pygame.quit()
sys.exit()
