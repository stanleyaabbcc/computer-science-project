import pygame
import random

FPS = 60
WIDTH = 500
HEIGHT = 600

GREEN = (0,255,0)
WHITE = (253,245,230)
RED = (255,0,0)

#遊戲初始化,遊戲視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT)) #視窗大小
clock = pygame.time.Clock()
pygame.display.set_caption("計概專題遊戲") #視窗命名
running = True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect() #定位物件
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
    def update(self):
        key_pressed = pygame.key.get_pressed() #檢視按鍵有沒有被按
        if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0    

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40))
        self.image.fill(RED)
        self.rect = self.image.get_rect() #定位物件
        self.rect.x = random.randrange(0 , WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100 , -40)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0 , WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100 , -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    r = Rock()
    all_sprites.add(r)

#建立遊戲迴圈
while running:
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #更新遊戲

    all_sprites.update()

    #畫面顯示
    screen.fill(WHITE) #改變遊戲顏色(後面是rgb值)
    all_sprites.draw(screen) #畫出所有在all_sprites裡的東西
    pygame.display.update() #更新畫面

pygame.quit()            