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
pygame.display.set_caption("Cas 9 - Slike u igrici")

clock = pygame.time.Clock()

# =====================
# BOJE
# =====================
WHITE = (255,255,255)
BLACK = (0,0,0)

# =====================
# FONT
# =====================
font = pygame.font.SysFont(None, 36)

# =====================
# UCITAVANJE SLIKA
# =====================
player_img = pygame.image.load("player.png")
coin_img = pygame.image.load("coin.png")
enemy_img = pygame.image.load("enemy.png")

# smanjenje slike
player_img = pygame.transform.scale(player_img,(50,50))
coin_img = pygame.transform.scale(coin_img,(30,30))
enemy_img = pygame.transform.scale(enemy_img,(60,40))

# =====================
# IGRAC
# =====================
player_rect = player_img.get_rect()
player_rect.center = (WIDTH//2, HEIGHT//2)

player_speed = 5

# =====================
# NOVCIC
# =====================
coin_rect = coin_img.get_rect()
coin_rect.topleft = (
    random.randint(0, WIDTH-30),
    random.randint(0, HEIGHT-30)
)

# =====================
# NEPRIJATELJ
# =====================
enemy_rect = enemy_img.get_rect()
enemy_rect.topleft = (200,200)

enemy_speed = 3
enemy_direction = 1

# =====================
# POENI
# =====================
score = 0

# =====================
# GAME LOOP
# =====================
running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # KRETANJE IGRACA
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

    # KRETANJE NEPRIJATELJA
    enemy_rect.y += enemy_speed * enemy_direction

    if enemy_rect.top <= 0 or enemy_rect.bottom >= HEIGHT:
        enemy_direction *= -1

    # SAKUPLJANJE
    if player_rect.colliderect(coin_rect):

        score += 1

        coin_rect.topleft = (
            random.randint(0, WIDTH-30),
            random.randint(0, HEIGHT-30)
        )

    # GAME OVER
    if player_rect.colliderect(enemy_rect):
        running = False

    # =====================
    # CRTANJE
    # =====================
    screen.fill(WHITE)

    screen.blit(player_img, player_rect)
    screen.blit(coin_img, coin_rect)
    screen.blit(enemy_img, enemy_rect)

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text,(10,10))

    pygame.display.update()

pygame.quit()
sys.exit()
