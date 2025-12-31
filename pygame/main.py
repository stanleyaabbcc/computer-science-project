import pygame
import random
import sys

# 初始化
pygame.init()

# 螢幕設定
WIDTH, HEIGHT = 480, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame 1945 飛機大戰")

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 時鐘
clock = pygame.time.Clock()
FPS = 60

# 載入圖片（如果你沒有圖片會用簡單色塊代替）
def load_image(path, size):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except:
        # 沒圖片就用色塊代替
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill((100, 100, 100, 200))
        return surf

# 背景（兩張無縫捲動）
bg1 = pygame.Surface((WIDTH, HEIGHT))
bg1.fill((135, 206, 235))  # 天空藍
bg2 = bg1.copy()
bg_y1 = 0
bg_y2 = -HEIGHT

# 玩家飛機
player_size = (60, 80)
player_img = load_image("player.png", player_size)  # 如有圖片放這
player_rect = player_img.get_rect()
player_rect.centerx = WIDTH // 2
player_rect.bottom = HEIGHT - 50
player_speed = 6

# 子彈
bullets = []
bullet_speed = -12
bullet_damage = 1

# 敵機
enemies = []
enemy_spawn_timer = 0
enemy_speed_base = 3

# 分數
score = 0
font = pygame.font.SysFont("microsoftyahei", 36)  # 中文支援更好

# 遊戲狀態
game_over = False

# 主循環
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                # 重玩
                score = 0
                bullets.clear()
                enemies.clear()
                player_rect.centerx = WIDTH // 2
                player_rect.bottom = HEIGHT - 50
                game_over = False

    if not game_over:
        # 玩家移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_rect.y += player_speed
            
        # 邊界限制
        player_rect.clamp_ip(screen.get_rect())

        # 射擊（按住空白鍵連射）
        if keys[pygame.K_SPACE]:
            if pygame.time.get_ticks() % 8 == 0:  # 控制射速
                bullet = pygame.Rect(player_rect.centerx - 3, player_rect.top, 6, 20)
                bullets.append(bullet)

        # 生成敵機
        enemy_spawn_timer += 1
        if enemy_spawn_timer > 40:  # 越玩越快可改這裡
            enemy_spawn_timer = 0
            enemy_size = (70, 70)
            enemy_img = load_image("enemy.png", enemy_size)
            enemy_rect = enemy_img.get_rect()
            enemy_rect.centerx = random.randint(30, WIDTH-30)
            enemy_rect.y = -80
            enemies.append(enemy_rect)

        # 更新子彈
        for b in bullets[:]:
            b.y += bullet_speed
            if b.bottom < 0:
                bullets.remove(b)

        # 更新敵機
        for e in enemies[:]:
            e.y += enemy_speed_base
            if e.top > HEIGHT:
                enemies.remove(e)

        # 碰撞檢測：子彈打敵機
        for b in bullets[:]:
            for e in enemies[:]:
                if b.colliderect(e):
                    bullets.remove(b)
                    enemies.remove(e)
                    score += 100
                    break

        # 碰撞檢測：玩家被撞
        for e in enemies:
            if e.colliderect(player_rect):
                game_over = True

    # ===== 繪製 =====
    # 捲動背景
    bg_y1 += 3
    bg_y2 += 3
    if bg_y1 >= HEIGHT: bg_y1 = -HEIGHT
    if bg_y2 >= HEIGHT: bg_y2 = -HEIGHT
    
    screen.blit(bg1, (0, bg_y1))
    screen.blit(bg2, (0, bg_y2))

    # 畫玩家
    if not game_over or pygame.time.get_ticks() % 600 < 300:  # 遊戲結束閃爍
        screen.blit(player_img, player_rect)

    # 畫子彈（黃色）
    for b in bullets:
        pygame.draw.rect(screen, (255, 255, 0), b)

    # 畫敵機（紅色色塊或圖）
    for e in enemies:
        screen.blit(enemy_img, e) if 'enemy_img' in locals() else pygame.draw.rect(screen, RED, e)

    # 分數
    score_text = font.render(f"分數: {score}", True, WHITE)    #True開啟反鋸齒
    screen.blit(score_text, (10, 10))

    # Game Over
    if game_over:
        go_text = font.render("GAME OVER - 按 R 重新開始", True, RED)    #True開啟反鋸齒
        screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//2 - 50))    #screen.blit顯示在

    pygame.display.flip()    #把剛剛畫好的所有東西，一次性全部顯示到螢幕上！

pygame.quit()
sys.exit()