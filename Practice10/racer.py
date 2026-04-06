import pygame
import sys
import random
import time
from pathlib import Path

pygame.init()

base = Path(__file__).resolve().parent
img = base / "im"

W, H = 400, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("My game")
clock = pygame.time.Clock()

speed = 5
coins = 0

font_path = base / "font_user.ttf"
if font_path.exists():
    big_font = pygame.font.Font(str(font_path), 60)
    small_font = pygame.font.Font(str(font_path), 20)
else:
    big_font = pygame.font.SysFont("arial", 60)
    small_font = pygame.font.SysFont("arial", 20)

bg = pygame.image.load(str(img / "AnimatedStreet.png"))
coin_icon = pygame.image.load(str(img / "Coin.png"))
coin_icon = pygame.transform.scale(coin_icon, (coin_icon.get_width() // 15, coin_icon.get_height() // 10))


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        path = img / "Enemy.png"
        if path.exists():
            self.image = pygame.image.load(str(path))
        else:
            self.image = pygame.Surface((50, 90))
            self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, W - 40), 0)

    def update(self):
        global speed
        self.rect.y += speed
        if self.rect.top > H:
            self.reset()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        path = img / "Player.png"
        if path.exists():
            self.image = pygame.image.load(str(path))
        else:
            self.image = pygame.Surface((50, 90))
            self.image.fill(BLUE)

        self.rect = self.image.get_rect(center=(160, 520))

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5

        if keys[pygame.K_RIGHT] and self.rect.right < W:
            self.rect.x += 5


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(str(img / "Coin.png"))
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 12, self.image.get_height() // 12))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, W - 40), 0)

    def update(self):
        self.rect.y += 5
        if self.rect.top > H:
            self.reset()


player = Player()
enemy = Enemy()
coin = Coin()

enemies = pygame.sprite.Group(enemy)
coins_group = pygame.sprite.Group(coin)
all_sprites = pygame.sprite.Group(player, enemy, coin)

add_speed = pygame.USEREVENT + 1
pygame.time.set_timer(add_speed, 4000)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == add_speed:
            speed += 1

    all_sprites.update()

    if pygame.sprite.spritecollideany(player, enemies):
        crash = img / "crash.wav"
        if crash.exists():
            pygame.mixer.Sound(str(crash)).play()

        time.sleep(0.5)

        screen.fill(RED)
        game_over_text = big_font.render("Game Over", True, BLACK)
        result_text = small_font.render(f"Your result: {coins}", True, BLACK)

        screen.blit(game_over_text, (30, 250))
        screen.blit(result_text, (120, 350))
        pygame.display.update()

        time.sleep(2)
        run = False

    if pygame.sprite.spritecollide(player, coins_group, False):
        coins += 1
        coin.reset()

    screen.blit(bg, (0, 0))
    screen.blit(coin_icon, (10, 35))

    coins_text = small_font.render(f"X{coins}", True, BLACK)
    screen.blit(coins_text, (50, 50))

    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()