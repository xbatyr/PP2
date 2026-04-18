import pygame
import random
import sys
import time

pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - Weighted Food with Timer")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 24)

class Snake:
    """Snake class handling movement and collision"""
    def __init__(self):
        self.positions = [
            [GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE],
            [GRID_WIDTH // 2 * GRID_SIZE - GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE],
            [GRID_WIDTH // 2 * GRID_SIZE - 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE]
        ]
        self.direction = RIGHT
        self.grow_flag = False
        self.color = GREEN
        self.head_color = (0, 200, 0)

    def move(self):
        """Move snake by adding new head and removing tail"""
        head = self.positions[0].copy()
        head[0] += self.direction[0] * GRID_SIZE
        head[1] += self.direction[1] * GRID_SIZE
        
        self.positions.insert(0, head)
        
        if not self.grow_flag:
            self.positions.pop()
        else:
            self.grow_flag = False

    def change_direction(self, new_direction):
        """Change direction preventing reverse"""
        if (new_direction[0] != -self.direction[0] or 
            new_direction[1] != -self.direction[1]):
            self.direction = new_direction

    def grow(self):
        """Set flag to grow on next move"""
        self.grow_flag = True

    def check_self_collision(self):
        """Check if head hits body"""
        head = self.positions[0]
        return head in self.positions[1:]

    def check_border_collision(self):
        """Check if snake leaves screen"""
        head = self.positions[0]
        return (head[0] < 0 or head[0] >= SCREEN_WIDTH or
                head[1] < 0 or head[1] >= SCREEN_HEIGHT)

    def draw(self, surface):
        """Draw snake on screen"""
        for i, pos in enumerate(self.positions):
            if i == 0:
                pygame.draw.rect(surface, self.head_color, 
                               (pos[0], pos[1], GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, WHITE, 
                               (pos[0], pos[1], GRID_SIZE, GRID_SIZE), 2)
            else:
                pygame.draw.rect(surface, self.color, 
                               (pos[0], pos[1], GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, BLACK, 
                               (pos[0], pos[1], GRID_SIZE, GRID_SIZE), 1)

class Food:
    """Food with different weights and expiration timer"""
    def __init__(self, snake_positions):
        self.position = [0, 0]
        self.respawn(snake_positions)

    def respawn(self, snake_positions):
        """Generate new food with random weight and set timer"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            
            if [x, y] not in snake_positions:
                self.position = [x, y]
                break
        
        # Random weight: 1, 2, or 3 (higher weight = more points)
        self.weight = random.choices([1, 2, 3], weights=[50, 35, 15])[0]
        self.set_color_by_weight()
        
        # Set expiration timer (5-10 seconds)
        self.spawn_time = time.time()
        self.lifetime = random.randint(5, 10)

    def set_color_by_weight(self):
        """Set food color based on weight"""
        if self.weight == 1:
            self.color = RED
        elif self.weight == 2:
            self.color = ORANGE
        else:
            self.color = GOLD

    def is_expired(self):
        """Check if food should disappear"""
        return time.time() - self.spawn_time > self.lifetime

    def get_remaining_time(self):
        """Get seconds until expiration"""
        return max(0, self.lifetime - (time.time() - self.spawn_time))

    def draw(self, surface):
        """Draw food with weight indicator"""
        # Draw food
        pygame.draw.rect(surface, self.color, 
                        (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, WHITE, 
                        (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE), 2)
        
        # Draw weight number
        weight_text = small_font.render(str(self.weight), True, BLACK)
        text_rect = weight_text.get_rect(center=(self.position[0] + GRID_SIZE//2, 
                                                  self.position[1] + GRID_SIZE//2))
        surface.blit(weight_text, text_rect)

def show_game_over(screen, score, level, total_weight):
    """Display game over screen with stats"""
    screen.fill(BLACK)
    
    game_over_text = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    level_text = font.render(f"Level Reached: {level}", True, YELLOW)
    weight_text = font.render(f"Total Weight: {total_weight}", True, GOLD)
    restart_text = font.render("Press SPACE to restart", True, GREEN)
    quit_text = font.render("Press ESC to quit", True, GREEN)
    
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 120))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 220))
    screen.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, 270))
    screen.blit(weight_text, (SCREEN_WIDTH//2 - weight_text.get_width()//2, 320))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 400))
    screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 450))
    
    pygame.display.flip()

def main():
    """Main game loop"""
    snake = Snake()
    food = Food(snake.positions)
    
    # Game variables
    score = 0
    level = 1
    foods_eaten = 0
    total_weight = 0
    FOODS_PER_LEVEL = 4  # Level up every 4 foods
    
    # Speed settings
    base_speed = 10
    current_speed = base_speed
    
    running = True
    game_active = True
    
    while running:
        clock.tick(current_speed)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_active:
                    # Arrow keys + WASD controls
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        snake.change_direction(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                else:
                    if event.key == pygame.K_SPACE:
                        # Restart game
                        snake = Snake()
                        food = Food(snake.positions)
                        score = 0
                        level = 1
                        foods_eaten = 0
                        total_weight = 0
                        current_speed = base_speed
                        game_active = True
                    elif event.key == pygame.K_ESCAPE:
                        running = False
        
        if game_active:
            snake.move()
            
            # Check if food expired
            if food.is_expired():
                food.respawn(snake.positions)
            
            # Check collisions
            if snake.check_border_collision() or snake.check_self_collision():
                game_active = False
                continue
            
            # Check if snake ate food
            if snake.positions[0] == food.position:
                snake.grow()
                score += food.weight * 10  # Weight multiplies score
                foods_eaten += 1
                total_weight += food.weight
                
                # Level up check
                if foods_eaten >= FOODS_PER_LEVEL:
                    level += 1
                    foods_eaten = 0
                    current_speed = base_speed + (level * 2)  # Increase speed
                
                food.respawn(snake.positions)
            
            # Draw everything
            screen.fill(BLACK)
            
            # Draw grid
            for x in range(0, SCREEN_WIDTH, GRID_SIZE):
                pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, SCREEN_HEIGHT))
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
                pygame.draw.line(screen, (20, 20, 20), (0, y), (SCREEN_WIDTH, y))
            
            snake.draw(screen)
            food.draw(screen)
            
            # UI Elements
            score_text = font.render(f"Score: {score}", True, WHITE)
            level_text = font.render(f"Level: {level}", True, YELLOW)
            speed_text = font.render(f"Speed: {current_speed}", True, CYAN)
            weight_text = font.render(f"Weight: {food.weight}", True, GOLD)
            timer_text = font.render(f"Expires: {food.get_remaining_time():.1f}s", True, ORANGE)
            foods_text = font.render(f"Next: {foods_eaten}/{FOODS_PER_LEVEL}", True, PURPLE)
            total_weight_text = small_font.render(f"Total Weight: {total_weight}", True, GOLD)
            
            # Display UI
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (10, 50))
            screen.blit(speed_text, (10, 90))
            screen.blit(weight_text, (10, 130))
            screen.blit(timer_text, (10, 170))
            screen.blit(foods_text, (10, 210))
            screen.blit(total_weight_text, (10, 250))
            
            # Controls hint
            controls_text = small_font.render("WASD / Arrows", True, WHITE)
            screen.blit(controls_text, (SCREEN_WIDTH - 150, 10))
            
            # Food value legend
            legend_y = SCREEN_HEIGHT - 80
            pygame.draw.rect(screen, (30, 30, 30), (SCREEN_WIDTH - 200, legend_y, 190, 75))
            pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 200, legend_y, 190, 75), 2)
            
            legend_title = small_font.render("Food Values:", True, WHITE)
            red_text = small_font.render("Red = 10 pts (W:1)", True, RED)
            orange_text = small_font.render("Orange = 20 pts (W:2)", True, ORANGE)
            gold_text = small_font.render("Gold = 30 pts (W:3)", True, GOLD)
            
            screen.blit(legend_title, (SCREEN_WIDTH - 190, legend_y + 5))
            screen.blit(red_text, (SCREEN_WIDTH - 190, legend_y + 25))
            screen.blit(orange_text, (SCREEN_WIDTH - 190, legend_y + 45))
            screen.blit(gold_text, (SCREEN_WIDTH - 190, legend_y + 60))
            
        else:
            show_game_over(screen, score, level, total_weight)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()