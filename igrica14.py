import pygame
import sys
import random

pygame.init()

# =====================
# EKRAN
# =====================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Full Game")

clock = pygame.time.Clock()

# =====================
# BOJE
# =====================
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,120,255)
GREEN = (0,180,0)
RED = (200,0,0)
YELLOW = (240,200,0)

font = pygame.font.SysFont(None, 32)

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
# GLOBAL
# =====================
level = 1
max_unlocked = 1
game_state = "menu"

inventory = {"coin": 0}

# =====================
# ORUZJA
# =====================
weapons = {
    "pistol": {"speed": 8, "damage": 1},
    "fast": {"speed": 12, "damage": 1},
    "strong": {"speed": 6, "damage": 2}
}

inventory_items = ["pistol", "fast", "strong"]
current_weapon = "pistol"
show_inventory = False

bullets = []

# =====================
# LEVEL DATA
# =====================
platforms = []
enemies = []
coins = []

boss = pygame.Rect(600, 480, 80, 60)
boss_hp = 20

def create_level(lvl):
    global platforms, enemies, coins, boss_hp

    platforms = []
    enemies = []
    coins = []

    # platforme
    for _ in range(lvl + 2):
        platforms.append(
            pygame.Rect(
                random.randint(100, 600),
                random.randint(200, 500),
                120,
                20
            )
        )

    # enemy
    for _ in range(lvl):
        enemies.append([
            pygame.Rect(random.randint(100,700),500,40,40),
            random.choice([-2,2])
        ])

    # coin
    for _ in range(3):
        coins.append(
            pygame.Rect(
                random.randint(100,700),
                random.randint(100,500),
                20,20
            )
        )

    boss_hp = 20


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

            # INVENTORY
            if event.key == pygame.K_i:
                show_inventory = not show_inventory

            # MENU
            if game_state == "menu":
                if pygame.K_1 <= event.key <= pygame.K_9:
                    selected = event.key - pygame.K_0
                    if selected <= max_unlocked:
                        level = selected
                        create_level(level)
                        game_state = "play"

                if event.key == pygame.K_0 and max_unlocked >= 10:
                    level = 10
                    create_level(level)
                    game_state = "play"

            # ESC → MENU
            if event.key == pygame.K_ESCAPE:
                game_state = "menu"

            # SKOK
            if event.key == pygame.K_SPACE :
                velocity_y = jump_strength

            # WASD PUCANJE
            if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:

                direction = [0, 0]

                if event.key == pygame.K_w:
                    direction = [0, -1]
                if event.key == pygame.K_s:
                    direction = [0, 1]
                if event.key == pygame.K_a:
                    direction = [-1, 0]
                if event.key == pygame.K_d:
                    direction = [1, 0]

                bullet = {
                    "rect": pygame.Rect(player.centerx, player.centery, 10, 10),
                    "dir": direction
                }

                bullets.append(bullet)

    # =====================
    # PLAY STATE
    # =====================
    if game_state == "play":

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed

        # GRAVITY
        velocity_y += gravity
        player.y += velocity_y

        on_ground = False

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

        # ENEMY
        for enemy in enemies[:]:
            enemy[0].x += enemy[1]

            if enemy[0].left <= 0 or enemy[0].right >= WIDTH:
                enemy[1] *= -1

            if player.colliderect(enemy[0]):
                player_hp -= 1
                player.topleft = (100,300)

        # COINS
        for coin in coins[:]:
            if player.colliderect(coin):
                inventory["coin"] += 1
                coins.remove(coin)

        # METCI
        for bullet in bullets[:]:
            speed = weapons[current_weapon]["speed"]

            bullet["rect"].x += bullet["dir"][0] * speed
            bullet["rect"].y += bullet["dir"][1] * speed

            # enemy hit
            for enemy in enemies[:]:
                if bullet["rect"].colliderect(enemy[0]):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break

            # boss hit
            if level == 10 and bullet["rect"].colliderect(boss):
                bullets.remove(bullet)
                boss_hp -= weapons[current_weapon]["damage"]

        bullets = [
            b for b in bullets
            if 0 < b["rect"].x < WIDTH and 0 < b["rect"].y < HEIGHT
        ]

        # BOSS
        if level == 10:
            boss.x += 3

            if boss.left <= 0 or boss.right >= WIDTH:
                boss.x = random.randint(100,700)

            if player.colliderect(boss):
                player_hp -= 1
                player.topleft = (100,300)

        # LEVEL UP
        if len(coins) == 0 and level < 10:
            level += 1
            if level > max_unlocked:
                max_unlocked = level
            create_level(level)

        # WIN / LOSE
        if level == 10 and boss_hp <= 0:
            game_state = "menu"

        if player_hp <= 0:
            game_state = "menu"
            player_hp = 5

    # =====================
    # CRTANJE
    # =====================
    screen.fill(WHITE)

    if game_state == "menu":
        y = 150
        for i in range(1,11):
            text = f"Level {i}"
            color = BLACK if i <= max_unlocked else (150,150,150)
            label = font.render(text, True, color)
            screen.blit(label, (300, y))
            y += 40

        info = font.render("1-9, 0 = Level 10", True, BLACK)
        screen.blit(info, (250, 100))

    elif game_state == "play":

        pygame.draw.rect(screen, BLUE, player)
        pygame.draw.rect(screen, GREEN, ground)

        for plat in platforms:
            pygame.draw.rect(screen, GREEN, plat)

        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy[0])

        for coin in coins:
            pygame.draw.rect(screen, YELLOW, coin)

        for bullet in bullets:
            pygame.draw.rect(screen, BLACK, bullet["rect"])

        if level == 10:
            pygame.draw.rect(screen, RED, boss)

        # HUD
        screen.blit(font.render(f"Level: {level}", True, BLACK),(10,10))
        screen.blit(font.render(f"HP: {player_hp}", True, BLACK),(10,40))
        screen.blit(font.render(f"Coins: {inventory['coin']}", True, BLACK),(10,70))
        screen.blit(font.render(f"Weapon: {current_weapon}", True, BLACK),(10,100))

    # INVENTORY UI
    if show_inventory:
        pygame.draw.rect(screen, (200,200,200), (150,100,500,400))

        y = 150
        for item in inventory_items:

            color = RED if item == current_weapon else BLACK
            text = font.render(item, True, color)
            rect = text.get_rect(center=(400, y))

            screen.blit(text, rect)

            if pygame.mouse.get_pressed()[0]:
                if rect.collidepoint(pygame.mouse.get_pos()):
                    current_weapon = item

            y += 60

    pygame.display.update()

pygame.quit()
sys.exit()
