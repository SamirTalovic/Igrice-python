import pygame
import sys

pygame.init()

# =====================
# EKRAN
# =====================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cas 19 - Kamera")

clock = pygame.time.Clock()

# =====================
# BOJE
# =====================
WHITE = (255,255,255)
BLUE = (0,120,255)
GREEN = (0,180,0)
RED = (200,0,0)

# =====================
# SVET (VEĆI OD EKRANA)
# =====================
WORLD_WIDTH = 2000

# =====================
# IGRAC (WORLD KOORDINATE)
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
ground = pygame.Rect(0, 550, WORLD_WIDTH, 50)

# =====================
# PLATFORME
# =====================
platforms = [
    pygame.Rect(300, 450, 150, 20),
    pygame.Rect(700, 350, 150, 20),
    pygame.Rect(1200, 400, 150, 20),
    pygame.Rect(1600, 300, 150, 20)
]

# =====================
# NEPRIJATELJ
# =====================
enemy = pygame.Rect(900, 500, 40, 40)
enemy_speed = 3
enemy_direction = 1

# =====================
# KAMERA
# =====================
camera_x = 0

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
    # KRETANJE
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

    # POD
    if player.colliderect(ground):
        player.bottom = ground.top
        velocity_y = 0
        on_ground = True

    # PLATFORME
    for plat in platforms:
        if player.colliderect(plat) and velocity_y > 0:
            player.bottom = plat.top
            velocity_y = 0
            on_ground = True

    # =====================
    # ENEMY
    # =====================
    enemy.x += enemy_speed * enemy_direction

    if enemy.left <= 800 or enemy.right >= 1200:
        enemy_direction *= -1

    # =====================
    # KAMERA PRATI IGRACA
    # =====================
    camera_x = player.x - WIDTH // 2

    # ogranicenje kamere
    if camera_x < 0:
        camera_x = 0
    if camera_x > WORLD_WIDTH - WIDTH:
        camera_x = WORLD_WIDTH - WIDTH

    # =====================
    # CRTANJE (OFFSET!)
    # =====================
    screen.fill(WHITE)

    # igrac
    pygame.draw.rect(screen, BLUE, (player.x - camera_x, player.y, 40, 50))

    # ground
    pygame.draw.rect(screen, GREEN, (ground.x - camera_x, ground.y, ground.width, ground.height))

    # platforme
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, (plat.x - camera_x, plat.y, plat.width, plat.height))

    # enemy
    pygame.draw.rect(screen, RED, (enemy.x - camera_x, enemy.y, enemy.width, enemy.height))

    pygame.display.update()

pygame.quit()
sys.exit()
