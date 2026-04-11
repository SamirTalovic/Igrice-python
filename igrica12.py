import pygame
import sys
import random

pygame.init()

# =====================
# EKRAN
# =====================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer - Boss Fight")

clock = pygame.time.Clock()

# =====================
# BOJE
# =====================
WHITE = (255,255,255)
BLUE = (0,120,255)
GREEN = (0,180,0)
RED = (200,0,0)
BLACK = (0,0,0)

font = pygame.font.SysFont(None, 36)

# =====================
# IGRAC
# =====================
player = pygame.Rect(100, 300, 40, 50)

player_speed = 5
velocity_y = 0

gravity = 0.5
jump_strength = -10

on_ground = False

player_hp = 5

# =====================
# POD
# =====================
ground = pygame.Rect(0, 550, 800, 50)

# =====================
# PLATFORME
# =====================
platforms = [
    pygame.Rect(200, 450, 150, 20),
    pygame.Rect(500, 350, 150, 20)
]

# =====================
# BOSS
# =====================
boss = pygame.Rect(500, 480, 80, 60)

boss_hp = 10
boss_speed = 3
boss_direction = 1

# =====================
# METCI
# =====================
bullets = []
bullet_speed = 10

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

            # PUCANJE
            if event.key == pygame.K_f:
                bullet = pygame.Rect(
                    player.centerx,
                    player.centery,
                    10,
                    5
                )
                bullets.append(bullet)

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
    # METCI
    # =====================
    for bullet in bullets:
        bullet.x += bullet_speed

    bullets = [b for b in bullets if b.x < WIDTH]

    # =====================
    # BOSS KRETANJE
    # =====================
    boss.x += boss_speed * boss_direction

    if boss.left <= 0 or boss.right >= WIDTH:
        boss_direction *= -1

    # =====================
    # METAK POGADJA BOSS
    # =====================
    for bullet in bullets:
        if bullet.colliderect(boss):
            bullets.remove(bullet)
            boss_hp -= 1

    # =====================
    # BOSS POGADJA IGRACA
    # =====================
    if player.colliderect(boss):
        player_hp -= 1
        player.x = 100
        player.y = 300
        pygame.time.delay(300)

    # =====================
    # GAME OVER / WIN
    # =====================
    if player_hp <= 0:
        print("GAME OVER")
        running = False

    if boss_hp <= 0:
        print("POBEDA!")
        running = False

    # =====================
    # CRTANJE
    # =====================
    screen.fill(WHITE)

    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, GREEN, ground)

    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)

    pygame.draw.rect(screen, RED, boss)

    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, bullet)

    # HP
    player_text = font.render(f"HP: {player_hp}", True, BLACK)
    boss_text = font.render(f"BOSS HP: {boss_hp}", True, BLACK)

    screen.blit(player_text, (10, 10))
    screen.blit(boss_text, (10, 40))

    pygame.display.update()

pygame.quit()
sys.exit()
