import random
import pygame

SCREEN_WIDTH = round(1920 * 0.9)
SCREEN_HEIGHT = round(1080 * 0.9)

class fruit:
    def __init__(self):
        self.x = SCREEN_WIDTH/4
        self.y = SCREEN_HEIGHT/4

    def draw(self, surface):
        pygame.draw.rect(surface, (228, 0, 0), (self.x, self.y, 37, 37))

class head:
    def __init__(self):
        self.x = SCREEN_WIDTH/2
        self.y = SCREEN_HEIGHT/2
        self.direction = None
        self.size = 37

    def handle_keys(self):
        key = pygame.key.get_pressed()

        if (key[ord('w')] or key[pygame.K_UP]) and self.direction != 'DOWN':
            self.direction = 'UP'
        elif (key[ord('s')] or key[pygame.K_DOWN]) and self.direction != 'UP':
            self.direction = 'DOWN'
        elif (key[ord('a')] or key[pygame.K_LEFT]) and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif (key[ord('d')] or key[pygame.K_RIGHT]) and self.direction != 'LEFT':
            self.direction = 'RIGHT'
        elif key[pygame.K_SPACE]:
            self.direction = None

    def draw(self, surface):
        global game_over
        distance = 5

        if self.direction == None:
            pass
        elif self.direction == 'UP':
            self.y -= distance
        elif self.direction == 'DOWN':
            self.y += distance
        elif self.direction == 'LEFT':
            self.x -= distance
        elif self.direction == 'RIGHT':
            self.x += distance

        if (self.x < 0 or self.x > SCREEN_WIDTH-self.size) or (self.y < 0 or self.y > SCREEN_HEIGHT-self.size):
            game_over = True
            self.direction = None

        pygame.draw.rect(surface, (0, 102, 0), (self.x, self.y, self.size, self.size))

class body:
    pass

def check_collision(snake, apple):
    apple_rect = pygame.Rect(apple.x, apple.y, 37, 37)
    snake_rect = pygame.Rect(snake.x, snake.y, 37, 37)
    return apple_rect.colliderect(snake_rect)

def update_fps():
	fps = str(int(clock.get_fps())) + ' fps'
	fps_text = fps_font.render(fps, True, pygame.Color("coral"))
	return fps_text

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snek")
clock = pygame.time.Clock()
running = True
game_over = False
fps_font = pygame.font.SysFont("Arial", 18)
game_over_font = pygame.font.SysFont("Arial", 120)
snake = head()
apple = fruit()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    if not game_over:
        snake.handle_keys()

        if check_collision(snake, apple):
            apple.x, apple.y = random.randint(0,SCREEN_WIDTH-37), random.randint(0,SCREEN_HEIGHT-37)
    else:
        game_over_text = game_over_font.render('Game over', True, pygame.Color("red"))
        game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(game_over_text, game_over_text_rect)

    apple.draw(screen)
    snake.draw(screen)
    screen.blit(update_fps(), (10,0))
    pygame.display.update()

    clock.tick(60)

pygame.quit()