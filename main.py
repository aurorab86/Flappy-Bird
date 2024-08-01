import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

background_img = pygame.image.load('image/background.png')
bird_img = pygame.image.load('image/bird.png')
pipe_img = pygame.image.load('image/pipe.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = bird_img
        self.image = pygame.transform.scale(self.image, (50, 35))
        self.rect = self.image.get_rect()
        self.rect.center = (50, SCREEN_HEIGHT // 2)
        self.gravity = 0.25
        self.velocity = 0

    def update(self):
        self.velocity += self.gravity
        self.rect.y += int(self.velocity)

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def flap(self):
        self.velocity = -5

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, is_top):
        super().__init__()
        self.image = pipe_img
        self.image = pygame.transform.scale(self.image, (80, 300))
        self.rect = self.image.get_rect()
        if is_top:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - 150)
        else:
            self.rect.topleft = (x, y + 150)

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()

bird = Bird()
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()
all_sprites.add(bird)

def create_pipes():
    y = random.randint(200, 400)
    top_pipe = Pipe(SCREEN_WIDTH, y, True)
    bottom_pipe = Pipe(SCREEN_WIDTH, y, False)
    all_sprites.add(top_pipe)
    all_sprites.add(bottom_pipe)
    pipes.add(top_pipe)
    pipes.add(bottom_pipe)

pipe_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_timer, 1500)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()
        if event.type == pipe_timer:
            create_pipes()

    all_sprites.update()


    if pygame.sprite.spritecollideany(bird, pipes):
        running = False

    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
