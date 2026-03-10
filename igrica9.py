import pygame
import sys
import random

pygame.init()

# =====================
# EKRAN
# =====================
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cas 11 - Shooting")

clock = pygame.time.Clock()

# =====================
# BOJE
# =====================
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
BLUE = (0,120,255)

font = pygame.font.SysFont(None,36)

# =====================
# IGRAC
# =====================
player_rect = pygame.Rect(400,500,40,40)
player_speed = 6

# =====================
# METCI
# =====================
bullets = []
bullet_speed = 8

# =====================
# NEPRIJATELJ
# =====================
enemy_rect = pygame.Rect(
    random.randint(0,750),
    50,
    50,
    40
)

enemy_speed = 3

score = 0

running = True

# =====================
# GAME LOOP
# =====================

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # PUCANJE
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                bullet = pygame.Rect(
                    player_rect.centerx - 5,
                    player_rect.top,
                    10,
                    20
                )

                bullets.append(bullet)

    # =====================
    # KRETANJE IGRACA
    # =====================

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed

    player_rect.clamp_ip(screen.get_rect())

    # =====================
    # KRETANJE METAKA
    # =====================

    for bullet in bullets:
        bullet.y -= bullet_speed

    bullets = [b for b in bullets if b.y > 0]

    # =====================
    # ENEMY
    # =====================

    enemy_rect.y += enemy_speed

    if enemy_rect.top > HEIGHT:

        enemy_rect.x = random.randint(0,750)
        enemy_rect.y = 0

    # =====================
    # SUDAR METAK - ENEMY
    # =====================

    for bullet in bullets:

        if bullet.colliderect(enemy_rect):

            bullets.remove(bullet)

            score += 1

            enemy_rect.x = random.randint(0,750)
            enemy_rect.y = 0

    # =====================
    # GAME OVER
    # =====================

    if player_rect.colliderect(enemy_rect):
        running = False

    # =====================
    # CRTANJE
    # =====================

    screen.fill(WHITE)

    pygame.draw.rect(screen, BLUE, player_rect)

    pygame.draw.rect(screen, RED, enemy_rect)

    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, bullet)

    score_text = font.render(f"Score: {score}",True,BLACK)
    screen.blit(score_text,(10,10))

    pygame.display.update()

pygame.quit()
sys.exit()
