import config
import assets

def draw_debug_info(screen, x, y, level, time_left, hero, enemy_group):
    """Отображает отладочную информацию, если config.DEBUG_MODE == True."""
    if not config.DEBUG_MODE:
        return

    enemy_count = len(enemy_group)
    if enemy_count > 0:
        hp_values = [e.hp for e in enemy_group]
        dmg_values = [e.damage for e in enemy_group]
        hp_min = min(hp_values)
        hp_max = max(hp_values)
        dmg_min = min(dmg_values)
        dmg_max = max(dmg_values)
    else:
        hp_min = 0
        hp_max = 0
        dmg_min = 0
        dmg_max = 0

    lines = [
        "--- ОТЛАДКА ---",
        f"Уровень = {level}",
        f"Таймер = {time_left}",
        f"Скорость героя = {hero.speed:.2f}",
        f"Урон героя = {hero.damage}",
        f"HP героя = {hero.hp}/{hero.max_hp}",
        f"Врагов = {enemy_count}",
        f"HP врагов: min={hp_min}, max={hp_max}",
        f"DMG врагов: min={dmg_min}, max={dmg_max}",
        "(Каждые 3 уровня уменьшается interval врагов)"
    ]
    for i, line in enumerate(lines):
        txt_surf = assets.mini_font.render(line, True, (150, 150, 150))
        screen.blit(txt_surf, (x, y + i * 18))
