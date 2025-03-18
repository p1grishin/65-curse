import pygame
import config

pygame.init()

# Создаём окно
if config.FULLSCREEN:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    config.SCREEN_WIDTH, config.SCREEN_HEIGHT = screen.get_size()
else:
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption("Curse of 65")
clock = pygame.time.Clock()

# Шрифты
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 20)
mini_font = pygame.font.Font(None, 18)

def load_scaled_image(path, size):
    """Пытается загрузить изображение path и масштабирует"""
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)
    return img

# Загружаем спрайты
try:
    player_image = load_scaled_image("assets/player.png", (40, 40))
    enemy_image  = load_scaled_image("assets/enemy.png", (30, 30))
    boss_image   = load_scaled_image("assets/boss.png",  (60, 60))
    bullet_image = load_scaled_image("assets/bullet.png",(10, 10))
    coin_image   = load_scaled_image("assets/coin.png",  (30, 30))
    boss_coin_image = load_scaled_image("assets/bosscoin.png", (45, 45))
    background_tile = load_scaled_image("assets/grass_tile.png", (config.TILE_SIZE, config.TILE_SIZE))
except:
    print("Не удалось загрузить спрайты. Используются заглушки.")

    player_image = pygame.Surface((40, 40))
    player_image.fill(config.WHITE)

    enemy_image = pygame.Surface((30, 30))
    enemy_image.fill((200, 0, 0))

    boss_image = pygame.Surface((60, 60))
    boss_image.fill((150, 0, 0))

    bullet_image = pygame.Surface((10, 10))
    bullet_image.fill(config.RED)

    coin_image = pygame.Surface((15, 15))
    coin_image.fill(config.GOLD)

    boss_coin_image = pygame.Surface((45, 45))
    boss_coin_image.fill((255, 225, 0))

    background_tile = pygame.Surface((config.TILE_SIZE, config.TILE_SIZE))
    background_tile.fill((34, 139, 34))
