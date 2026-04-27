import random
import sys
import time

import pygame


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - Weighted Food with Timer")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 24)


class Snake:
    def __init__(self):
        self.positions = [
            [GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE],
            [GRID_WIDTH // 2 * GRID_SIZE - GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE],
            [GRID_WIDTH // 2 * GRID_SIZE - 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE],
        ]
        self.direction = RIGHT
        self.grow_flag = False
        self.color = GREEN
        self.head_color = (0, 200, 0)

    def move(self):
        head = self.positions[0].copy()
        head[0] += self.direction[0] * GRID_SIZE
        head[1] += self.direction[1] * GRID_SIZE
        self.positions.insert(0, head)

        if not self.grow_flag:
            self.positions.pop()
        else:
            self.grow_flag = False

    def change_direction(self, new_direction):
        # stop instant reverse
        if new_direction[0] != -self.direction[0] or new_direction[1] != -self.direction[1]:
            self.direction = new_direction

    def grow(self):
        self.grow_flag = True

    def hits_self(self):
        return self.positions[0] in self.positions[1:]

    def hits_border(self):
        head = self.positions[0]
        return head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT

    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            color = self.head_color if i == 0 else self.color
            border = WHITE if i == 0 else BLACK
            border_size = 2 if i == 0 else 1
            pygame.draw.rect(surface, color, (pos[0], pos[1], GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, border, (pos[0], pos[1], GRID_SIZE, GRID_SIZE), border_size)


class Food:
    def __init__(self, snake_positions):
        self.position = [0, 0]
        self.respawn(snake_positions)

    def respawn(self, snake_positions):
        # find free cell for new food
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if [x, y] not in snake_positions:
                self.position = [x, y]
                break

        self.weight = random.choices([1, 2, 3], weights=[50, 35, 15])[0]
        self.color = RED if self.weight == 1 else ORANGE if self.weight == 2 else GOLD
        self.spawn_time = time.time()
        self.lifetime = random.randint(5, 10)

    def is_expired(self):
        return time.time() - self.spawn_time > self.lifetime

    def remaining_time(self):
        return max(0, self.lifetime - (time.time() - self.spawn_time))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, WHITE, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE), 2)
        image = small_font.render(str(self.weight), True, BLACK)
        surface.blit(image, image.get_rect(center=(self.position[0] + GRID_SIZE // 2, self.position[1] + GRID_SIZE // 2)))


def show_game_over(score, level, total_weight):
    screen.fill(BLACK)
    screen.blit(big_font.render("GAME OVER", True, RED), (SCREEN_WIDTH // 2 - 180, 120))
    screen.blit(font.render(f"Final Score: {score}", True, WHITE), (SCREEN_WIDTH // 2 - 110, 220))
    screen.blit(font.render(f"Level Reached: {level}", True, YELLOW), (SCREEN_WIDTH // 2 - 125, 270))
    screen.blit(font.render(f"Total Weight: {total_weight}", True, GOLD), (SCREEN_WIDTH // 2 - 115, 320))
    screen.blit(font.render("Press SPACE to restart", True, GREEN), (SCREEN_WIDTH // 2 - 145, 400))
    screen.blit(font.render("Press ESC to quit", True, GREEN), (SCREEN_WIDTH // 2 - 115, 450))
    pygame.display.flip()


def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (20, 20, 20), (0, y), (SCREEN_WIDTH, y))


def draw_ui(score, level, current_speed, food, foods_eaten, foods_per_level, total_weight):
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Level: {level}", True, YELLOW), (10, 50))
    screen.blit(font.render(f"Speed: {current_speed}", True, CYAN), (10, 90))
    screen.blit(font.render(f"Weight: {food.weight}", True, GOLD), (10, 130))
    screen.blit(font.render(f"Expires: {food.remaining_time():.1f}s", True, ORANGE), (10, 170))
    screen.blit(font.render(f"Next: {foods_eaten}/{foods_per_level}", True, PURPLE), (10, 210))
    screen.blit(small_font.render(f"Total Weight: {total_weight}", True, GOLD), (10, 250))
    screen.blit(small_font.render("WASD / Arrows", True, WHITE), (SCREEN_WIDTH - 150, 10))

    legend_y = SCREEN_HEIGHT - 80
    pygame.draw.rect(screen, (30, 30, 30), (SCREEN_WIDTH - 200, legend_y, 190, 75))
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 200, legend_y, 190, 75), 2)
    screen.blit(small_font.render("Food Values:", True, WHITE), (SCREEN_WIDTH - 190, legend_y + 5))
    screen.blit(small_font.render("Red = 10 pts (W:1)", True, RED), (SCREEN_WIDTH - 190, legend_y + 25))
    screen.blit(small_font.render("Orange = 20 pts (W:2)", True, ORANGE), (SCREEN_WIDTH - 190, legend_y + 45))
    screen.blit(small_font.render("Gold = 30 pts (W:3)", True, GOLD), (SCREEN_WIDTH - 190, legend_y + 60))


def main():
    snake = Snake()
    food = Food(snake.positions)

    score = 0
    level = 1
    foods_eaten = 0
    total_weight = 0
    foods_per_level = 4
    base_speed = 10
    current_speed = base_speed

    running = True
    game_active = True

    while running:
        clock.tick(current_speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if game_active:
                    # controls
                    if event.key in (pygame.K_UP, pygame.K_w):
                        snake.change_direction(UP)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        snake.change_direction(DOWN)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        snake.change_direction(LEFT)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        snake.change_direction(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                else:
                    # restart after game over
                    if event.key == pygame.K_SPACE:
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

            if food.is_expired():
                food.respawn(snake.positions)

            if snake.hits_border() or snake.hits_self():
                game_active = False
                continue

            if snake.positions[0] == food.position:
                snake.grow()
                score += food.weight * 10
                foods_eaten += 1
                total_weight += food.weight

                if foods_eaten >= foods_per_level:
                    level += 1
                    foods_eaten = 0
                    current_speed = base_speed + level * 2

                food.respawn(snake.positions)

            screen.fill(BLACK)
            draw_grid()
            snake.draw(screen)
            food.draw(screen)
            draw_ui(score, level, current_speed, food, foods_eaten, foods_per_level, total_weight)
        else:
            show_game_over(score, level, total_weight)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
