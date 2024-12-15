import pygame
import sys
import random
pygame.init()
#replace the image source with respectiv name
bird_image = pygame.image.load("OIP.JPEG")
bird_image = pygame.transform.scale(bird_image, (30, 30))
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
clock = pygame.time.Clock()
gravity = 0.5
bird_movement = 0
pipe_speed = 4
pipe_gap = 150
pipe_width = 50
pipes = []
score = 0
font = pygame.font.Font(None, 36)
bird = pygame.Rect(WIDTH // 4, HEIGHT // 2, 30, 30)
base = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)
def create_pipe():
    height = random.randint(150, 400)
    top_pipe = {"pipe": pygame.Rect(WIDTH, height - pipe_gap - 200, pipe_width, 200), "scored": False}
    bottom_pipe = {"pipe": pygame.Rect(WIDTH, height, pipe_width, HEIGHT - height - 50), "scored": False}
    return top_pipe, bottom_pipe
def move_pipes(pipes):
    for pipe_pair in pipes:
        pipe_pair["pipe"].centerx -= pipe_speed

    return [pipe for pipe in pipes if pipe["pipe"].right > 0]
def draw_pipes(pipes):
    for pipe_pair in pipes:
        pipe = pipe_pair["pipe"]
        if pipe.bottom >= HEIGHT:
            pygame.draw.rect(screen, GREEN, pipe)
        else:
            pygame.draw.rect(screen, RED, pipe)
def check_collision(pipes):
    for pipe_pair in pipes:
        if bird.colliderect(pipe_pair["pipe"]):
            return False
    if bird.top <= 0 or bird.bottom >= HEIGHT - 50:
        return False

    return True

def display_score(score):
    score_surface = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_surface, (10, 10))
pipe_timer = pygame.USEREVENT
pygame.time.set_timer(pipe_timer, 1200)
running = True
while running:
    screen.fill(BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = -8
        if event.type == pipe_timer:
            pipes.extend(create_pipe())
    bird_movement += gravity
    bird.centery += bird_movement
    pipes = move_pipes(pipes)
    for pipe_pair in pipes:
        pipe = pipe_pair["pipe"]
        if not pipe_pair["scored"] and bird.centerx > pipe.centerx:
            score += 1
            pipe_pair["scored"] = True
    if not check_collision(pipes):
        running = False
    screen.blit(bird_image, bird)
    draw_pipes(pipes)
    pygame.draw.rect(screen, BLACK, base)
    display_score(score//2)
    pygame.display.update()
    clock.tick(30)
