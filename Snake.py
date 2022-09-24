import random
import pygame

SCREEN_X = round(1920 * 0.9)
SCREEN_Y = round(1080 * 0.9)


class fruit:
    def __init__(self):
        self.x = SCREEN_X/4
        self.y = SCREEN_Y/4

    def draw(self, surface):
        pygame.draw.rect(surface, (228, 0, 0), (self.x, self.y, 37, 37))

class head:
    def __init__(self):
        self.x = SCREEN_X/2
        self.y = SCREEN_Y/2
        self.direction = None

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
        distance = 0.6

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

        pygame.draw.rect(surface, (0, 102, 0), (self.x, self.y, 37, 37))


class body:
    pass


def check_collision(snake, apple):
    apple_rect = pygame.Rect(apple.x, apple.y, 37, 37)
    snake_rect = pygame.Rect(snake.x, snake.y, 37, 37)
    return apple_rect.colliderect(snake_rect)

pygame.init()
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
pygame.display.set_caption("Snak")
running = True

snake = head()
apple = fruit()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    snake.handle_keys()
    screen.fill((255, 255, 255))
    apple.draw(screen)
    snake.draw(screen)
    pygame.display.update()
    if check_collision(snake, apple):
        apple.x, apple.y = random.randint(0,SCREEN_X-37), random.randint(0,SCREEN_Y-37)

pygame.quit()
