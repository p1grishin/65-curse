import pygame
import math
import config
import assets

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, max_hp, hp=None, damage=10, coins=0,
                 cost_str=None, cost_agi=None, cost_end=None):
        super().__init__()
        self.image = assets.player_image
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = speed
        self.max_hp = max_hp
        self.hp = hp if hp is not None else self.max_hp
        self.damage = damage
        self.coins = coins

        # Стоимость апгрейдов
        self.cost_str = float(config.UPGRADE_COST_BASE) if cost_str is None else cost_str
        self.cost_agi = float(config.UPGRADE_COST_BASE) if cost_agi is None else cost_agi
        self.cost_end = float(config.UPGRADE_COST_BASE) if cost_end is None else cost_end

    def update(self, dt, keys):
        vel_x = 0
        vel_y = 0
        if keys[pygame.K_w]:
            vel_y -= self.speed
        if keys[pygame.K_s]:
            vel_y += self.speed
        if keys[pygame.K_a]:
            vel_x -= self.speed
        if keys[pygame.K_d]:
            vel_x += self.speed

        self.rect.x += vel_x
        self.rect.y += vel_y

        # Границы мира
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.right > config.WORLD_WIDTH:
            self.rect.right = config.WORLD_WIDTH
        if self.rect.bottom > config.WORLD_HEIGHT:
            self.rect.bottom = config.WORLD_HEIGHT

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_x, direction_y, damage):
        super().__init__()
        self.image = assets.bullet_image
        self.rect = self.image.get_rect(center=(x, y))

        length = math.hypot(direction_x, direction_y)
        if length == 0:
            length = 1
        self.dx = (direction_x / length) * config.BULLET_SPEED
        self.dy = (direction_y / length) * config.BULLET_SPEED
        self.damage = damage

    def update(self, dt):
        self.rect.x += self.dx
        self.rect.y += self.dy
        # Удаляем пулю, если она вышла за границы
        if (self.rect.right < 0 or self.rect.left > config.WORLD_WIDTH or
            self.rect.top < 0   or self.rect.bottom > config.WORLD_HEIGHT):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, hp, damage, speed, is_boss=False, attack_interval=1000):
        super().__init__()
        self.image = assets.boss_image if is_boss else assets.enemy_image
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.is_boss = is_boss

        # атака с задержкой
        self.attack_interval = attack_interval  # (мс)
        self.last_attack_time = 0

    def update(self, dt, player):
        direction = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(self.x, self.y)
        distance = direction.length()
        if distance > 0:
            direction = direction.normalize()
            self.x += direction.x * self.speed
            self.y += direction.y * self.speed
        self.rect.center = (int(self.x), int(self.y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, value=config.COIN_VALUE):
        super().__init__()
        self.image = assets.coin_image
        self.rect = self.image.get_rect(center=(x, y))
        self.value = value

class BossCoin(pygame.sprite.Sprite):
    def __init__(self, x, y, value=15):
        super().__init__()
        self.image = assets.boss_coin_image
        self.rect = self.image.get_rect(center=(x, y))
        self.value = value

class Camera:
    def __init__(self, width, height):
        self.offset_x = 0
        self.offset_y = 0
        self.width = width
        self.height = height

    def apply(self, rect):
        return rect.move(-self.offset_x, -self.offset_y)

    def update(self, target):
        w, h = assets.screen.get_size()
        config.SCREEN_WIDTH, config.SCREEN_HEIGHT = w, h

        self.offset_x = target.rect.centerx - config.SCREEN_WIDTH // 2
        self.offset_y = target.rect.centery - config.SCREEN_HEIGHT // 2
        if self.offset_x < 0:
            self.offset_x = 0
        if self.offset_y < 0:
            self.offset_y = 0
        max_x = self.width - config.SCREEN_WIDTH
        max_y = self.height - config.SCREEN_HEIGHT
        if self.offset_x > max_x:
            self.offset_x = max_x
        if self.offset_y > max_y:
            self.offset_y = max_y
