import pygame
import time
import random

pygame.init()

WIDTH = 680
HEIGHT = 440

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.display.set_caption('snake')
game_window = pygame.display.set_mode((WIDTH, HEIGHT))
fps = pygame.time.Clock()

# Initializing game state
snake_position = [100, 50]
snake_body = [[100, 50], [80, 50], [60, 50]]
direction = 'RIGHT'
change_to = direction

# Initial fruit position
fruit_position = [random.randrange(1, (WIDTH // 10)) * 10,
                  random.randrange(1, (HEIGHT // 10)) * 10]
fruit_spawn = True

# Game stats
score = 0
level = 1
snake_speed = 13  # Slightly faster base speed

# Display the score and level
def show_info(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f'Score: {score}  Level: {level}', True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

# End the game
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (WIDTH / 2, HEIGHT / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Preventing the snake from moving in the opposite direction instantly
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Updating the snake's head position
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Inserting new position into snake body
    snake_body.insert(0, list(snake_position))

    # Checking if fruit is eaten
    if snake_position == fruit_position:
        score += 10
        fruit_spawn = False
        # Increase level every 30 points
        if score % 30 == 0:
            level += 1
            snake_speed += 3
    else:
        snake_body.pop()

    # Generate new fruit position that doesn't overlap snake
    if not fruit_spawn:
        while True:
            fruit_position = [random.randrange(1, (WIDTH // 10)) * 10,
                              random.randrange(1, (HEIGHT // 10)) * 10]
            if fruit_position not in snake_body:
                break
    fruit_spawn = True

    # Game background
    game_window.fill(black)

    # Drawing the snake
    for pos in snake_body:
        pygame.draw.rect(game_window, blue, pygame.Rect(pos[0], pos[1], 10, 10))

    # Drawing the fruit
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # Checking for wall collision
    if snake_position[0] < 0 or snake_position[0] >= WIDTH:
        game_over()
    if snake_position[1] < 0 or snake_position[1] >= HEIGHT:
        game_over()

    # Checking for self collision
    for block in snake_body[1:]:
        if snake_position == block:
            game_over()

    # Showing score and level
    show_info(white, 'times new roman', 20)
    pygame.display.update()

    # Controlling the game speed
    fps.tick(snake_speed)