import random
import pygame

SCREEN_WIDTH = 30*55
SCREEN_HEIGHT = 18*55
MULTS = [i*55 for i in range(30)]

class QueueEmptyError(Exception):
    pass

class queue:
    def __init__(self):
        self._queue = []

    def __repr__(self):
        return f'{self._queue}'

    def isempty(self):
        return True if len(self._queue) == 0 else False

    def enqueue(self, data):
        self._queue.append(data)
        # print(f'enqueue, {self._queue=}')

    def dequeue(self):
        if self.isempty():
            raise QueueEmptyError
        temp = self._queue[0]
        self._queue.pop(0)
        # print(f'dequeue, {self._queue=}')
        return temp

    def peek(self):
        if self.isempty():
            raise QueueEmptyError
        return self._queue[0]

class fruit:
    def __init__(self):
        x, y = grid(17*55, 8*55)
        rect = pygame.Rect(0, 0, 40, 40)
        rect.center = x, y
        self.x, self.y = rect.topleft

        # self.x = SCREEN_WIDTH/4
        # self.y = SCREEN_HEIGHT/4
        self.size = 40

    def draw(self, surface):
        pygame.draw.rect(surface, (228, 0, 0), (self.x, self.y, self.size, self.size))

class body:
    def __init__(self):
        self.x, self.y = grid(9*55, 8*55)
        self.direction = None
        self.width = 40
        self.queue = queue()
        self.length = 1
        self.points = []
        self.direction_map = {'UP': (0, self.width), 'DOWN': (0, -self.width), 'LEFT': (self.width, 0), 'RIGHT': (-self.width, 0)}

    def move(self, key):
        if (key == (ord('w') or pygame.K_UP)) and self.direction != 'DOWN':
            self.queue.enqueue('UP')
        elif (key == (ord('s') or pygame.K_DOWN)) and self.direction != 'UP':
            self.queue.enqueue('DOWN')
        elif (key == (ord('a') or pygame.K_LEFT)) and self.direction != 'RIGHT':
            self.queue.enqueue('LEFT')
        elif (key == (ord('d') or pygame.K_RIGHT)) and self.direction != 'LEFT':
            self.queue.enqueue('RIGHT')
        elif key == pygame.K_SPACE:
            self.queue.enqueue(None)

    def handle_queue(self):
        if (not self.queue.isempty()) and ((self.x, self.y) == (grid(self.x, self.y))):
                command = '_'
                while command == self.direction:
                    command = self.queue.dequeue()

                self.direction = command
                try:
                    if self.points[-1] != (self.x, self.y):
                        self.points.append((self.x, self.y))
                        print(self.points)
                except IndexError:
                    print('except')
                    self.points.append((self.x, self.y))
                    print(self.points)

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

        rect = pygame.Rect(0,0,self.width, self.width)
        rect.center = self.x, self.y
        if (rect.x < 0 or rect.x > SCREEN_WIDTH-self.width) or (rect.y < 0 or rect.y > SCREEN_HEIGHT-self.width):
            game_over = True
            self.direction = None

        rect = pygame.Rect(0, 0, self.width, self.width)
        rect.center = self.x, self.y

        # Draw Head
        pygame.draw.rect(surface, (40, 104, 222), rect)
        pygame.draw.circle(surface, (0, 255, 0), (self.x, self.y), 4)

        # Draw Body
        for i in range(self.length-1):
            rect.center = (sum(x) for i in zip(self.direction_map[],3) )       #OVER HERE
            pygame.draw.rect(surface, (245, 141, 15), rect)


def check_collision(snake, apple):
    apple_rect = pygame.Rect(apple.x, apple.y, apple.size, apple.size)
    snake_rect = pygame.Rect(snake.x-20, snake.y-20, snake.width, snake.width)
    return apple_rect.colliderect(snake_rect)

def update_fps():
    fps = str(int(clock.get_fps())) + ' fps'
    fps_text = hud.render(fps, True, pygame.Color("coral"))
    return fps_text

def update_score():
    score_text = f'Score: {score}'
    rendered_score = hud.render(score_text, True, pygame.Color("coral"))
    return rendered_score

def grid(x, y):
    for num in MULTS:
        if abs(num-x) < 55/2:
            x = num
            break

    for num in MULTS:
        if abs(num-y) < 55/2:
            y = num
            break

    rect = pygame.Rect(x, y, 55, 55)
    return rect.centerx, rect.centery

def draw_bg(surface):
    bg_rect = pygame.Rect(0, 0, 55, 55)
    for j in range(9):
        for i in range(15):
            pygame.draw.rect(surface, (167,217,72), bg_rect) # Light Green
            bg_rect.centerx += 55
            pygame.draw.rect(surface, (142,204,57), bg_rect) # Dark Green
            bg_rect.centerx += 55

        bg_rect.centerx = 55/2
        bg_rect.centery += 55

        for i in range(15):
            pygame.draw.rect(surface, (142,204,57), bg_rect) # Dark Green
            bg_rect.centerx += 55
            pygame.draw.rect(surface, (167,217,72), bg_rect) # Light Green
            bg_rect.centerx += 55

        bg_rect.centerx = 55/2
        bg_rect.centery += 55

pygame.init()
pygame.key.set_repeat()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snek")
clock = pygame.time.Clock()
running = True
game_over = False
score = 0

snake = body()
apple = fruit()

hud = pygame.font.SysFont("Arial", 18)
game_over_font = pygame.font.SysFont("Arial", 120)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            snake.move(event.key)

    draw_bg(screen)
    if not game_over:
        snake.handle_queue()

        if check_collision(snake, apple):
            score += 1
            snake.length += 1
            x, y = grid(random.randint(0, SCREEN_WIDTH-apple.size), random.randint(0, SCREEN_HEIGHT-apple.size))
            rect = pygame.Rect(0, 0, 40, 40)
            rect.center = x, y
            apple.x, apple.y = rect.topleft
    else:
        game_over_text = game_over_font.render('Game over', True, pygame.Color("red"))
        game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(game_over_text, game_over_text_rect)

    apple.draw(screen)
    snake.draw(screen)
    screen.blit(update_fps(), (10, 0))
    screen.blit(update_score(), (10, 20))
    pygame.display.update()

    clock.tick(60)

pygame.quit()