#!usr/bin/python3
import pygame
import random
import os

WIDTH = 540
HEIGHT = 720
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
clock = pygame.time.Clock()

game_folder = os.path.dirname(__file__)
img_dir = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(img_dir, 'paddle.png')).convert()
ball_img = pygame.image.load(os.path.join(img_dir, 'ball.png')).convert()
cords = [-10, -9, -8, -7, -6, -5, -3, -4, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
random.shuffle(cords)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (100, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 50)
        self.speedx = 0
        self.shield = 100

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx -= 8
        if keystate[pygame.K_d]:
            self.speedx += 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ball_img, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.top = HEIGHT - (HEIGHT - 20)
        self.speedy = 10
        self.speedx = cords[0]

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speedx = random.randrange(-10, -3)
            if self.rect.top < 30:
                self.rect.top = 30
                self.speedy = 10

        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx = random.randrange(3, 10)
            if self.rect.top < 0:
                self.rect.top = 0
                self.speedy = 10
        if self.rect.top < 30:
            self.rect.top = 30
            self.speedy = 10


score = 0

all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
player = Player()
ball = Ball()
all_sprites.add(ball)
balls.add(ball)
all_sprites.add(player)

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if ball.rect.bottom > HEIGHT:
        player.shield -= random.randint(33, 34)
        ball = Ball()
        all_sprites.add(ball)
        balls.add(ball)
        if player.shield <= 0:
            running = False
    collide = pygame.sprite.spritecollide(player, balls, False)
    if collide:
        score += 100
        ball.speedy = -10

    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    pygame.display.flip()
    player.update()
    balls.update()

pygame.quit()
