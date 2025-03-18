import pygame
import config
import screens
import game

def main():
    choice = screens.start_menu()
    if choice is None:
        pygame.quit()
        return

    if choice == "new":
        game.game_loop(
            level=1,
            hero_hp=config.INITIAL_PLAYER_HP,
            hero_maxhp=config.INITIAL_PLAYER_HP,
            hero_speed=config.INITIAL_PLAYER_SPEED,
            hero_damage=config.INITIAL_PLAYER_DAMAGE,
            hero_coins=0
        )
    elif choice == "load":
        loaded = game.load_game()
        if loaded is None:
            # Нет сохранения - начнём новую
            game.game_loop(1, config.INITIAL_PLAYER_HP, config.INITIAL_PLAYER_HP,
                           config.INITIAL_PLAYER_SPEED, config.INITIAL_PLAYER_DAMAGE, 0)
        else:
            level, hero_par = loaded
            game.game_loop(
                level,
                hero_par["hp"],
                hero_par["max_hp"],
                hero_par["speed"],
                hero_par["damage"],
                hero_par["coins"],
                cost_str=hero_par.get("cost_str", config.UPGRADE_COST_BASE),
                cost_agi=hero_par.get("cost_agi", config.UPGRADE_COST_BASE),
                cost_end=hero_par.get("cost_end", config.UPGRADE_COST_BASE)
            )

if __name__ == "__main__":
    main()
