import pygame
import config
import assets

class Button:
    def __init__(self, x, y, w, h, text, font, bg_color=config.GRAY, text_color=config.WHITE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=6)
        render_text = self.font.render(self.text, True, self.text_color)
        text_rect = render_text.get_rect(center=self.rect.center)
        surface.blit(render_text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def show_shop(player, screen, level):
    box_width = 500
    box_height = 450
    box_x = config.SCREEN_WIDTH // 2 - box_width // 2
    box_y = config.SCREEN_HEIGHT // 2 - box_height // 2

    plus_btn_size = 30
    row_gap = 70

    str_y = box_y + 80
    strength_btn = Button(box_x + box_width - 60, str_y, plus_btn_size, plus_btn_size, "+", assets.small_font)

    agi_y = str_y + row_gap
    agility_btn = Button(box_x + box_width - 60, agi_y, plus_btn_size, plus_btn_size, "+", assets.small_font)

    end_y = agi_y + row_gap
    endurance_btn = Button(box_x + box_width - 60, end_y, plus_btn_size, plus_btn_size, "+", assets.small_font)

    # Выйти (сохранить)
    save_btn_w = 200
    save_btn_h = 40
    save_btn_x = box_x + box_width // 2 - save_btn_w // 2
    save_btn_y = box_y + box_height - 60
    save_btn = Button(save_btn_x, save_btn_y, save_btn_w, save_btn_h, "Выйти (сохранить)", assets.small_font)

    # Продолжить
    next_btn_w = 150
    next_btn_h = 40
    next_btn_x = box_x + box_width // 2 - next_btn_w // 2
    next_btn_y = box_y + box_height - 110
    next_btn = Button(next_btn_x, next_btn_y, next_btn_w, next_btn_h, "Продолжить", assets.small_font)

    shop_open = True
    while shop_open:
        screen.fill(config.BLACK)

        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(config.DARK_GRAY)
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, config.BLACK, (box_x, box_y, box_width, box_height), border_radius=20)

        title_text = assets.font.render("Магазин", True, config.WHITE)
        screen.blit(title_text, (box_x + box_width // 2 - title_text.get_width() // 2, box_y + 20))

        # Сила
        current_str = player.damage
        next_str = player.damage + config.UPGRADE_AMOUNT['strength']
        str_line = f"Сила: {current_str} => {next_str}"
        str_cost_text = f"Стоимость: {int(player.cost_str)} монет"

        str_surf = assets.small_font.render(str_line, True, config.WHITE)
        str_cost_surf = assets.small_font.render(str_cost_text, True, config.GOLD)
        screen.blit(str_surf, (box_x + 30, str_y))
        screen.blit(str_cost_surf, (box_x + 30, str_y + 25))
        strength_btn.draw(screen)

        # Ловкость
        current_agi = player.speed
        next_agi = player.speed + config.UPGRADE_AMOUNT['agility']
        agi_line = f"Ловкость: {current_agi:.1f} => {next_agi:.1f}"
        agi_cost_text = f"Стоимость: {int(player.cost_agi)} монет"

        agi_surf = assets.small_font.render(agi_line, True, config.WHITE)
        agi_cost_surf = assets.small_font.render(agi_cost_text, True, config.GOLD)
        screen.blit(agi_surf, (box_x + 30, agi_y))
        screen.blit(agi_cost_surf, (box_x + 30, agi_y + 25))
        agility_btn.draw(screen)

        # Выносливость
        current_end = player.max_hp
        next_end = player.max_hp + config.UPGRADE_AMOUNT['endurance']
        end_line = f"Выносливость: {current_end} => {next_end}"
        end_cost_text = f"Стоимость: {int(player.cost_end)} монет"

        end_surf = assets.small_font.render(end_line, True, config.WHITE)
        end_cost_surf = assets.small_font.render(end_cost_text, True, config.GOLD)
        screen.blit(end_surf, (box_x + 30, end_y))
        screen.blit(end_cost_surf, (box_x + 30, end_y + 25))
        endurance_btn.draw(screen)

        coins_text = f"Ваши монеты: {player.coins}"
        coins_surf = assets.small_font.render(coins_text, True, config.GOLD)
        screen.blit(coins_surf, (box_x + box_width // 2 - coins_surf.get_width() // 2, box_y + box_height - 140))

        next_btn.draw(screen)
        save_btn.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                if strength_btn.is_clicked((mx, my)):
                    c = int(player.cost_str)
                    if player.coins >= c:
                        player.damage += config.UPGRADE_AMOUNT['strength']
                        player.coins -= c
                        player.cost_str += config.UPGRADE_COST_DELTA

                if agility_btn.is_clicked((mx, my)):
                    c = int(player.cost_agi)
                    if player.coins >= c:
                        player.speed += config.UPGRADE_AMOUNT['agility']
                        player.coins -= c
                        player.cost_agi += config.UPGRADE_COST_DELTA

                if endurance_btn.is_clicked((mx, my)):
                    c = int(player.cost_end)
                    if player.coins >= c:
                        player.max_hp += config.UPGRADE_AMOUNT['endurance']
                        player.hp += config.UPGRADE_AMOUNT['endurance']
                        player.coins -= c
                        player.cost_end += config.UPGRADE_COST_DELTA

                if next_btn.is_clicked((mx, my)):
                    shop_open = False

                if save_btn.is_clicked((mx, my)):
                    from game import save_game
                    save_game(level, player)
                    pygame.quit()
                    exit()
