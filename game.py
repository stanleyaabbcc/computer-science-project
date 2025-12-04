import pygame

#遊戲初始化,遊戲視窗
pygame.init
screen = pygame.display.set_mode((500,600))
clock = pygame.time.Clock()
fps = 1
running = True

#建立遊戲迴圈
while running:
    clock.tick(fps)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #更新遊戲

pygame.quit()            