import pygame

# 1. Pokretanje pygame-a
pygame.init()

# 2. Pravljenje prozora
WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moja prva igrica")

# 3. Boje (R, G, B)
BLACK = (0, 0, 0)
GREEN = (0, 255, 255)

# 4. Igrac
player_size = 40
player_x = WIDTH // 2
player_y = HEIGHT // 2
speed = 5

# 5. Sat za brzinu igre
clock = pygame.time.Clock()

# 6. Glavna petlja igre
running = True
while running:
    clock.tick(60)  # 60 FPS

    # 7. Dogadjaji (zatvaranje prozora)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 8. Pritisnuti tasteri
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player_x -= speed
    if keys[pygame.K_d]:
        player_x += speed
    if keys[pygame.K_w]:
        player_y -= speed
    if keys[pygame.K_s]:
        player_y += speed

    # 9. Granice ekrana
    if player_x < 0:
        player_x = 0
    if player_x > WIDTH - player_size:
        player_x = WIDTH - player_size
    if player_y < 0:
        player_y = 0
    if player_y > HEIGHT - player_size:
        player_y = HEIGHT - player_size

    # 10. Crtanje
    screen.fill(BLACK)
    pygame.draw.rect(
        screen,
        GREEN,
        (player_x, player_y, player_size, player_size)
    )
    pygame.draw.rect(
        screen,GREEN,
        (player_x + 50,player_y + 50,player_size,player_size)
    )
    # 11. Osvezavanje ekrana
    pygame.display.update()

# 12. Gasenje pygame-a
pygame.quit()
