# Imports
import pygame
import sys
from pygame.locals import *
import random
import time
import os

pygame.init()

# Game settings
FPS = 60
clock = pygame.time.Clock()

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# Screen and game variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
speed = 5
score = 0
coins_collected = 0
coin_weight_total = 0
coins_for_speedup = 5

# Fonts
big_font = pygame.font.SysFont("Verdana", 60)
small_font = pygame.font.SysFont("Verdana", 20)
medium_font = pygame.font.SysFont("Verdana", 30)
tiny_font = pygame.font.SysFont("Verdana", 15)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Street Racer - Weighted Coins")

# Load game images
def load_image(filename, color_fallback=None, width=50, height=50):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, filename)
    try:
        if os.path.exists(path):
            image = pygame.image.load(path)
        else:
            image = pygame.image.load(filename)
        return pygame.transform.scale(image, (width, height))
    except:
        image = pygame.Surface((width, height))
        image.fill(color_fallback or GRAY)
        return image

# Load all images
background_img = load_image("AnimatedStreet.png", GRAY, SCREEN_WIDTH, SCREEN_HEIGHT)
player_img = load_image("Player.png", BLUE, 50, 80)
enemy_img = load_image("Enemy.png", RED, 50, 80)


# Player class
class Player:
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
        self.speed = 7

    def move(self):
        keys = pygame.key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Enemy class
class Enemy:
    def __init__(self):
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.base_speed = speed
        self.reset()

    def reset(self):
        self.rect.x = random.randint(40, SCREEN_WIDTH - 40)
        self.rect.y = 0

    def move(self):
        global score
        current_speed = self.get_current_speed()
        self.rect.y += current_speed
        if self.rect.y > SCREEN_HEIGHT:
            score += 1
            self.reset()

    def get_current_speed(self):
        global coins_collected, coins_for_speedup
        speed_multiplier = 1 + (coins_collected // coins_for_speedup) * 0.2
        return self.base_speed * speed_multiplier

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Coin class
class Coin:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 25, 25)
        self.spawn_delay = random.randint(60, 180)
        self.active = False
        self.delay = 0
        self.weight = 1
        self.reset()

    def create_image(self):
        size = 25 + self.weight * 3
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        color = BRONZE if self.weight == 1 else SILVER if self.weight == 2 else GOLD
        pygame.draw.circle(self.image, color, (size//2, size//2), size//2)
        pygame.draw.circle(self.image, WHITE, (size//2, size//2), size//2, 2)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def reset(self):
        self.rect.x = random.randint(30, SCREEN_WIDTH - 30)
        self.rect.y = random.randint(-500, -100)
        self.weight = random.choices([1, 2, 3], weights=[50, 30, 20])[0]
        self.create_image()
        self.active = True

    def move(self):
        if not self.active:
            self.delay -= 1
            if self.delay <= 0:
                self.active = True
                self.delay = random.randint(120, 300)
            return
        self.rect.y += speed // 2
        if self.rect.y > SCREEN_HEIGHT:
            self.active = False
            self.reset()

    def draw(self, surface):
        if self.active:
            surface.blit(self.image, self.rect)
            weight_text = tiny_font.render(str(self.weight), True, BLACK)
            text_rect = weight_text.get_rect(center=self.rect.center)
            surface.blit(weight_text, text_rect)


# Game over screen
def show_game_over(final_score, final_coins, final_weight):
    screen.fill(RED)
    game_over_text = big_font.render("GAME OVER", True, BLACK)
    score_text = medium_font.render(f"Score: {final_score}", True, WHITE)
    coins_text = medium_font.render(f"Coins: {final_coins}", True, YELLOW)
    weight_text = small_font.render(f"Total Weight: {final_weight}", True, WHITE)
    restart_text = small_font.render("SPACE to restart", True, GREEN)
    quit_text = small_font.render("ESC to quit", True, GREEN)
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 150))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 250))
    screen.blit(coins_text, (SCREEN_WIDTH//2 - coins_text.get_width()//2, 290))
    screen.blit(weight_text, (SCREEN_WIDTH//2 - weight_text.get_width()//2, 330))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 400))
    screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 440))

# Reset game to initial state
def reset_game():
    global score, coins_collected, speed, coin_weight_total
    score = 0
    coins_collected = 0
    coin_weight_total = 0
    speed = 5
    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
    enemy.reset()
    coin.reset()


# Initialize game objects
player = Player()
enemy = Enemy()
coin = Coin()

game_over = False
speed_timer = 0
background_y = 0


# Main game loop
while True:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and game_over:
            if event.key == K_SPACE:
                reset_game()
                game_over = False
            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    if not game_over:
        # Update game state
        player.move()
        enemy.move()
        coin.move()
        
        # Gradually increase game speed
        speed_timer += 1
        if speed_timer > 300:
            speed = min(speed + 0.2, 12)
            speed_timer = 0
        
        # Check coin collection
        if coin.active and player.rect.colliderect(coin.rect):
            coins_collected += 1
            coin_weight_total += coin.weight
            score += coin.weight * 10
            coin.active = False
            coin.reset()
        
        # Check collision with enemy
        if player.rect.colliderect(enemy.rect):
            game_over = True
        
        # Draw background with scrolling effect
        background_y = (background_y + 2) % SCREEN_HEIGHT
        screen.blit(background_img, (0, background_y - SCREEN_HEIGHT))
        screen.blit(background_img, (0, background_y))
        
        # Draw game objects
        player.draw(screen)
        enemy.draw(screen)
        coin.draw(screen)
        
        # Render UI text
        score_text = small_font.render(f"Score: {score}", True, BLACK)
        coins_text = small_font.render(f"Coins: {coins_collected}", True, BLACK)
        weight_text = small_font.render(f"Weight: {coin_weight_total}", True, BLACK)
        speed_text = small_font.render(f"Speed: {enemy.get_current_speed():.1f}x", True, RED)
        next_speed_text = tiny_font.render(f"Next: {(coins_collected // coins_for_speedup + 1) * coins_for_speedup} coins", True, RED)
        
        # Draw UI background box
        pygame.draw.rect(screen, WHITE, (5, 5, 180, 115))
        pygame.draw.rect(screen, BLACK, (5, 5, 180, 115), 2)
        
        # Display UI text
        screen.blit(score_text, (10, 10))
        screen.blit(coins_text, (10, 35))
        screen.blit(weight_text, (10, 60))
        screen.blit(speed_text, (10, 80))
        screen.blit(next_speed_text, (10, 100))

    else:
        # Show game over screen
        show_game_over(score, coins_collected, coin_weight_total)
    
    pygame.display.update()