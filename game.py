import pygame
import json
import os
import random
import math

import config
import assets
import entities
import debug_info
import shop
import screens

def save_game(level, hero):
    data = {
        "level": level,
        "hero": {
            "speed": hero.speed,
            "max_hp": hero.max_hp,
            "hp": hero.hp,
            "damage": hero.damage,
            "coins": hero.coins,
            # цены из магазина
            "cost_str": hero.cost_str,
            "cost_agi": hero.cost_agi,
            "cost_end": hero.cost_end
        }
    }
    with open(config.SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Игра сохранена в", config.SAVE_FILE)

def load_game():
    if not os.path.exists(config.SAVE_FILE):
        return None
    try:
        with open(config.SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            level = data["level"]
            hero_params = data["hero"]
            return (level, hero_params)
    except:
        return None

def spawn_enemy(level, player_x, player_y):
    """Спавнит обычного врага для указанного уровня."""
    hp = config.ENEMY_BASE_HP + level * 2
    damage = config.ENEMY_BASE_DAMAGE + (level // 2)
    speed = config.ENEMY_BASE_SPEED + (level - 1) * 0.05

    steps = level // 3
    base_interval = 1000
    sub = steps * 200
    final_interval = max(200, base_interval - sub)

    angle = random.uniform(0, 2 * math.pi)
    dist = random.uniform(config.ENEMY_SPAWN_RADIUS * 0.8, config.ENEMY_SPAWN_RADIUS * 1.2)
    spawn_x = player_x + dist * math.cos(angle)
    spawn_y = player_y + dist * math.sin(angle)

    enemy = entities.Enemy(spawn_x, spawn_y, hp, damage, speed,
                           is_boss=False,
                           attack_interval=final_interval)
    return enemy

def spawn_boss(level, player_x, player_y):
    """Спавнит босса"""
    base_hp     = config.ENEMY_BASE_HP + level * 2
    base_damage = config.ENEMY_BASE_DAMAGE + (level // 2)
    base_speed  = config.ENEMY_BASE_SPEED + (level - 1) * 0.05

    boss_hp     = int(base_hp * config.BOSS_POWER_MULT)
    boss_damage = int(base_damage * config.BOSS_POWER_MULT)
    boss_speed  = base_speed

    steps = level // 3
    base_interval = 1000
    sub = steps * 200
    final_interval = max(200, base_interval - sub)

    angle = random.uniform(0, 2 * math.pi)
    dist = random.uniform(config.ENEMY_SPAWN_RADIUS * 0.8, config.ENEMY_SPAWN_RADIUS * 1.2)
    spawn_x = player_x + dist * math.cos(angle)
    spawn_y = player_y + dist * math.sin(angle)

    boss = entities.Enemy(spawn_x, spawn_y,
                          hp=boss_hp,
                          damage=boss_damage,
                          speed=boss_speed,
                          is_boss=True,
                          attack_interval=final_interval)
    return boss

def level_time(level):
    """Сколько времени длится уровень, зависит от того, сколько раз
       level делится на config.LEVEL_INCREASE_INTERVAL."""
    bonus_times = (level // config.LEVEL_INCREASE_INTERVAL) * config.LEVEL_TIME_INCREASE
    return config.LEVEL_DURATION + bonus_times


def game_loop(level, hero_hp, hero_maxhp, hero_speed, hero_damage, hero_coins,
              cost_str=None, cost_agi=None, cost_end=None):
    """
      - На кратном 5 уровне (5,10,15...) после окончания таймера появляется босс.
      - После убийства босса выпадает большая монета BossCoin (value=15).
      - Уровень завершается ТОЛЬКО когда игрок подберёт эту большую монету (или умрёт).
    """
    hero = entities.Player(
        x = config.WORLD_WIDTH // 2,
        y = config.WORLD_HEIGHT // 2,
        speed = hero_speed,
        max_hp = hero_maxhp,
        hp = hero_hp,
        damage = hero_damage,
        coins = hero_coins,
        cost_str = cost_str,
        cost_agi = cost_agi,
        cost_end = cost_end
    )

    camera = entities.Camera(config.WORLD_WIDTH, config.WORLD_HEIGHT)

    bullet_group = pygame.sprite.Group()
    enemy_group  = pygame.sprite.Group()
    coin_group   = pygame.sprite.Group()

    time_left = level_time(level)
    shoot_cooldown = config.AUTOFIRE_INTERVAL
    shoot_timer = 0.0

    boss_active = False
    boss_spawned = False
    boss_defeated = False

    last_time = pygame.time.get_ticks()
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    running = True
    while running:
        now = pygame.time.get_ticks()
        dt_ms = now - last_time
        dt = dt_ms / 1000.0
        last_time = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE and not config.FULLSCREEN:
                new_w, new_h = event.size
                config.SCREEN_WIDTH, config.SCREEN_HEIGHT = new_w, new_h
                assets.screen = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    screens.pause_menu(level, hero)
            elif event.type == pygame.USEREVENT:
                if time_left > 0:
                    time_left -= 1

        # Логика таймера
        if time_left <= 0:
            if level % config.BOSS_EVERY_X_LEVELS == 0:
                if not boss_spawned and not boss_active and not boss_defeated:
                    # чистим обычных
                    for e in enemy_group:
                        e.kill()
                    # спавн босса
                    b = spawn_boss(level, hero.rect.centerx, hero.rect.centery)
                    enemy_group.add(b)
                    boss_active = True
                    boss_spawned = True
            else:
                # Не боссовый уровень
                level += 1
                enemy_group.empty()
                bullet_group.empty()
                coin_group.empty()

                hero.hp = hero.max_hp
                shop.show_shop(hero, assets.screen, level)
                time_left = level_time(level)

        if boss_active:
            boss_exists = any(e.is_boss for e in enemy_group)
            if not boss_exists:
                boss_active = False
                boss_defeated = True
                # Большая монета создаётся ниже, в столкновении с пулей, когда hp<=0

        # Спавн обычных врагов
        if time_left > 0 and not boss_active and not boss_defeated:
            if len(enemy_group) < level * 3:
                enemy_group.add(spawn_enemy(level, hero.rect.centerx, hero.rect.centery))

        # Автострельба
        shoot_timer += dt
        if shoot_timer >= shoot_cooldown:
            if len(enemy_group) > 0:
                # найти ближайшего
                nearest = None
                best_dist = float('inf')
                for e in enemy_group:
                    dx = e.rect.centerx - hero.rect.centerx
                    dy = e.rect.centery - hero.rect.centery
                    dist_sq = dx*dx + dy*dy
                    if dist_sq < best_dist:
                        best_dist = dist_sq
                        nearest = e
                if nearest:
                    dir_x = nearest.rect.centerx - hero.rect.centerx
                    dir_y = nearest.rect.centery - hero.rect.centery
                    bullet = entities.Bullet(hero.rect.centerx, hero.rect.centery, dir_x, dir_y, hero.damage)
                    bullet_group.add(bullet)
            shoot_timer = 0.0

        # Обновление
        keys = pygame.key.get_pressed()
        hero.update(dt, keys)
        bullet_group.update(dt)
        for en in enemy_group:
            en.update(dt, hero)

        # Столкновение: герой vs враги
        current_time = pygame.time.get_ticks()
        collided_enemies = pygame.sprite.spritecollide(hero, enemy_group, False)
        for en in collided_enemies:
            if current_time - en.last_attack_time >= en.attack_interval:
                hero.take_damage(en.damage)
                en.last_attack_time = current_time
                # отталкивание
                direction = pygame.math.Vector2(hero.rect.center) - pygame.math.Vector2(en.rect.center)
                if direction.length() > 0:
                    direction = direction.normalize()
                    hero.rect.x += int(direction.x * 10)
                    hero.rect.y += int(direction.y * 10)

        # Столкновение: пули vs враги
        for b in bullet_group:
            hits = pygame.sprite.spritecollide(b, enemy_group, False)
            if hits:
                b.kill()
                for en in hits:
                    en.hp -= b.damage
                    if en.hp <= 0:
                        ex, ey = en.rect.center
                        if en.is_boss:
                            boss_active = False
                            boss_defeated = True
                            # создаём большую монету:
                            big_coin = entities.BossCoin(ex, ey, 15)
                            coin_group.add(big_coin)
                        else:
                            # обычная монета
                            coin_group.add(entities.Coin(ex, ey, config.COIN_VALUE))
                        en.kill()

        # Сбор монет
        collected_coins = pygame.sprite.spritecollide(hero, coin_group, True)
        for c in collected_coins:
            hero.coins += c.value
            # если это босс-монета
            if c.value == 15 and boss_defeated:
                boss_defeated = False
                boss_spawned = False
                level += 1

                enemy_group.empty()
                bullet_group.empty()
                coin_group.empty()

                hero.hp = hero.max_hp
                shop.show_shop(hero, assets.screen, level)
                time_left = level_time(level)

        # Смерть героя
        if hero.hp <= 0:
            restart = screens.show_game_over_screen()
            if restart:
                return game_loop(1, config.INITIAL_PLAYER_HP, config.INITIAL_PLAYER_HP,
                                 config.INITIAL_PLAYER_SPEED, config.INITIAL_PLAYER_DAMAGE, 0)
            else:
                running = False

        camera.update(hero)

        assets.screen.fill(config.BLACK)
        # Рисуем фон
        for tile_y in range(0, config.WORLD_HEIGHT, config.TILE_SIZE):
            for tile_x in range(0, config.WORLD_WIDTH, config.TILE_SIZE):
                r = assets.background_tile.get_rect(topleft=(tile_x, tile_y))
                r = camera.apply(r)
                if (r.right >= 0 and r.left <= config.SCREEN_WIDTH and
                    r.bottom >= 0 and r.top <= config.SCREEN_HEIGHT):
                    assets.screen.blit(assets.background_tile, r)

        # Рисуем пули
        for bullet in bullet_group:
            assets.screen.blit(bullet.image, camera.apply(bullet.rect))
        # Рисуем врагов
        for en in enemy_group:
            assets.screen.blit(en.image, camera.apply(en.rect))
        # Рисуем монеты
        for coin in coin_group:
            assets.screen.blit(coin.image, camera.apply(coin.rect))
        # Рисуем героя
        assets.screen.blit(hero.image, camera.apply(hero.rect))

        # UI
        lvl_text = assets.font.render(f"Уровень: {level}", True, config.WHITE)
        hp_text  = assets.font.render(f"Здоровье: {hero.hp}/{hero.max_hp}", True, config.GREEN)
        coins_text = assets.font.render(f"Монеты: {hero.coins}", True, config.GOLD)

        assets.screen.blit(lvl_text, (10,  10))
        assets.screen.blit(hp_text,  (10,  50))
        assets.screen.blit(coins_text, (10, 90))

        time_text = assets.font.render(f"Время: {time_left}", True, config.WHITE)
        assets.screen.blit(time_text, (config.SCREEN_WIDTH//2 - time_text.get_width()//2, 10))

        # Отладка
        debug_info.draw_debug_info(assets.screen, config.SCREEN_WIDTH - 280, 10, level, time_left, hero, enemy_group)

        pygame.display.flip()
        assets.clock.tick(config.FPS)

    pygame.quit()
