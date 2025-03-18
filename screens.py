import pygame
import config
import assets

def start_menu():
    from game import load_game
    run = True
    loaded_data = load_game()
    can_load = (loaded_data is not None)

    new_button_rect = pygame.Rect(config.SCREEN_WIDTH // 2 - 100, config.SCREEN_HEIGHT // 2 - 60, 200, 50)
    load_button_rect = pygame.Rect(config.SCREEN_WIDTH // 2 - 100, config.SCREEN_HEIGHT // 2 + 10, 200, 50)

    while run:
        assets.screen.fill(config.DARK_GRAY)
        title_text = assets.font.render("Curse of 65", True, config.WHITE)
        assets.screen.blit(title_text, (config.SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        pygame.draw.rect(assets.screen, (70, 70, 70), new_button_rect, border_radius=10)
        new_text = assets.font.render("Новая игра", True, config.WHITE)
        assets.screen.blit(new_text, (new_button_rect.centerx - new_text.get_width() // 2,
                                      new_button_rect.centery - new_text.get_height() // 2))

        pygame.draw.rect(assets.screen, (70, 70, 70), load_button_rect, border_radius=10)
        load_label = "Загрузить" if can_load else "Нет сохранений"
        load_color = config.WHITE if can_load else (150, 150, 150)
        load_text = assets.font.render(load_label, True, load_color)
        assets.screen.blit(load_text, (load_button_rect.centerx - load_text.get_width() // 2,
                                       load_button_rect.centery - load_text.get_height() // 2))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if new_button_rect.collidepoint(mx, my):
                    return "new"
                if load_button_rect.collidepoint(mx, my) and can_load:
                    return "load"

    return None

def show_game_over_screen():
    assets.screen.fill(config.DARK_GRAY)
    pygame.draw.rect(assets.screen, config.BLACK,
                     (config.SCREEN_WIDTH // 2 - 200, config.SCREEN_HEIGHT // 2 - 100, 400, 200),
                     border_radius=20)

    title_font = pygame.font.Font(None, 50)
    game_over_text = title_font.render("Игра Окончена", True, config.RED)
    restart_text = assets.font.render("R - начать заново", True, config.WHITE)
    quit_text = assets.font.render("Q - выйти", True, config.WHITE)

    rect_center_x = config.SCREEN_WIDTH // 2
    rect_center_y = config.SCREEN_HEIGHT // 2

    assets.screen.blit(game_over_text, (rect_center_x - game_over_text.get_width() // 2, rect_center_y - 60))
    assets.screen.blit(restart_text,   (rect_center_x - restart_text.get_width() // 2,   rect_center_y - 10))
    assets.screen.blit(quit_text,      (rect_center_x - quit_text.get_width() // 2,      rect_center_y + 30))

    pygame.display.flip()
    waiting = True
    restart = False
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart = True
                    waiting = False
                elif event.key == pygame.K_q:
                    restart = False
                    waiting = False
    return restart

def pause_menu(level, hero):
    paused = True
    while paused:
        # Затемняем фон
        assets.screen.fill(config.DARK_GRAY)

        # Рисуем прямоугольник-«окно» для паузы
        rect_w = 440
        rect_h = 200
        rect_x = config.SCREEN_WIDTH // 2 - rect_w // 2
        rect_y = config.SCREEN_HEIGHT // 2 - rect_h // 2
        pygame.draw.rect(assets.screen, config.BLACK, (rect_x, rect_y, rect_w, rect_h), border_radius=20)

        pause_text = assets.font.render("Пауза", True, config.WHITE)

        resume_text = assets.small_font.render("Нажмите P или ESC для продолжения", True, config.WHITE)

        level_text = assets.font.render(f"Уровень: {level}", True, config.WHITE)

        hero_stats_line = (
            f"HP: {hero.hp}/{hero.max_hp} | "
            f"Урон: {hero.damage} | "
            f"Скорость: {hero.speed:.1f} | "
            f"Монеты: {hero.coins}"
        )
        hero_stats_text = assets.small_font.render(hero_stats_line, True, config.GREEN)

        # Рассчитываем координаты центра «окна»
        rcx = rect_x + rect_w // 2
        rcy = rect_y + rect_h // 2

        # Выводим строки по вертикали с отступами
        assets.screen.blit(pause_text, (rcx - pause_text.get_width() // 2, rect_y + 20))
        assets.screen.blit(level_text, (rcx - level_text.get_width() // 2, rect_y + 70))
        assets.screen.blit(hero_stats_text, (rcx - hero_stats_text.get_width() // 2, rect_y + 110))
        assets.screen.blit(resume_text, (rcx - resume_text.get_width() // 2, rect_y + 150))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # По Esc или P выходим из паузы
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    paused = False

