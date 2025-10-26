import pygame
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game - Enhanced")

# Colors
BG_COLOR = (40, 40, 60)
GRID_COLOR = (60, 60, 90)
SNAKE_COLOR = [(0, 255, 100), (0, 200, 150), (0, 150, 200)]
FOOD_COLOR = (255, 80, 80)
TEXT_COLOR = (255, 255, 255)

# Font
font = pygame.font.SysFont("consolas", 24)

# Clock for speed
clock = pygame.time.Clock()

# Load sounds

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def draw_snake(snake):
    for i, (x, y) in enumerate(snake):
        color = SNAKE_COLOR[i % len(SNAKE_COLOR)]
        pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, (0, 0, 0), (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4))

def draw_food(food):
    pygame.draw.circle(screen, FOOD_COLOR, (food[0] + CELL_SIZE//2, food[1] + CELL_SIZE//2), CELL_SIZE//2 - 2)

def show_text(text, size, color, pos):
    font_obj = pygame.font.SysFont("consolas", size, bold=True)
    label = font_obj.render(text, True, color)
    screen.blit(label, pos)

def main():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "RIGHT"
    food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
    score = 0
    speed = 12

    running = True
    while running:
        screen.fill(BG_COLOR)
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        x, y = snake[0]
        if direction == "UP":
            y -= CELL_SIZE
        elif direction == "DOWN":
            y += CELL_SIZE
        elif direction == "LEFT":
            x -= CELL_SIZE
        elif direction == "RIGHT":
            x += CELL_SIZE

        new_head = (x, y)
        snake.insert(0, new_head)

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or new_head in snake[1:]:
            pygame.mixer.Sound.play(game_over_sound)
            game_over_screen(score)
            main()

        if new_head == food:
            score += 10
            pygame.mixer.Sound.play(eat_sound)
            food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
            if score % 50 == 0:  # Increase speed every 50 points
                speed += 2
        else:
            snake.pop()

        draw_snake(snake)
        draw_food(food)
        show_text(f"Score: {score}", 24, TEXT_COLOR, (10, 10))

        pygame.display.flip()
        clock.tick(speed)

def game_over_screen(score):
    screen.fill((20, 20, 30))
    show_text("GAME OVER!", 50, (255, 60, 60), (WIDTH//2 - 150, HEIGHT//2 - 80))
    show_text(f"Your Score: {score}", 35, (255, 255, 255), (WIDTH//2 - 120, HEIGHT//2))
    show_text("Press SPACE to Restart or ESC to Quit", 20, (200, 200, 200), (WIDTH//2 - 180, HEIGHT//2 + 60))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()
