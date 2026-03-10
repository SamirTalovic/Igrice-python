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
pygame.display.set_caption("Cas 10 - Animacija")

clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)

font = pygame.font.SysFont(None,36)

# =====================
# UCITAVANJE SLIKA
# =====================

walk1 = pygame.image.load("mario1.png")
walk2 = pygame.image.load("mario2.png")
walk3 = pygame.image.load("mario3.png")

coin_img = pygame.image.load("coin.png")
enemy_img = pygame.image.load("enemy.png")

walk1 = pygame.transform.scale(walk1,(50,50))
walk2 = pygame.transform.scale(walk2,(50,50))
walk3 = pygame.transform.scale(walk3,(50,50))

coin_img = pygame.transform.scale(coin_img,(30,30))
enemy_img = pygame.transform.scale(enemy_img,(60,40))

# lista animacije
player_frames = [walk1, walk2, walk3]

current_frame = 0
animation_speed = 0.15

# =====================
# IGRAC
# =====================

player_rect = walk1.get_rect()
player_rect.center = (WIDTH//2, HEIGHT//2)

player_speed = 5

# =====================
# COIN
# =====================

coin_rect = coin_img.get_rect()
coin_rect.topleft = (
    random.randint(0,WIDTH-30),
    random.randint(0,HEIGHT-30)
)

# =====================
# ENEMY
# =====================

enemy_rect = enemy_img.get_rect()
enemy_rect.topleft = (300,200)

enemy_speed = 3
enemy_direction = 1

score = 0

running = True

# =====================
# GAME LOOP
# =====================

while running:

    clock.tick(60)

    moving = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
        moving = True

    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
        moving = True

    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
        moving = True

    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed
        moving = True

    player_rect.clamp_ip(screen.get_rect())

    # =====================
    # ANIMACIJA
    # =====================

    if moving:
        current_frame += animation_speed

        if current_frame >= len(player_frames):
            current_frame = 0

    player_image = player_frames[int(current_frame)]

    # =====================
    # ENEMY KRETANJE
    # =====================

    enemy_rect.y += enemy_speed * enemy_direction

    if enemy_rect.top <= 0 or enemy_rect.bottom >= HEIGHT:
        enemy_direction *= -1

    # =====================
    # COIN
    # =====================

    if player_rect.colliderect(coin_rect):

        score += 1

        coin_rect.topleft = (
            random.randint(0,WIDTH-30),
            random.randint(0,HEIGHT-30)
        )

    # =====================
    # GAME OVER
    # =====================

    if player_rect.colliderect(enemy_rect):
        running = False

    # =====================
    # CRTANJE
    # =====================

    screen.fill(WHITE)

    screen.blit(player_image, player_rect)
    screen.blit(coin_img, coin_rect)
    screen.blit(enemy_img, enemy_rect)

    score_text = font.render(f"Score: {score}",True,BLACK)
    screen.blit(score_text,(10,10))

    pygame.display.update()

pygame.quit()
sys.exit()
