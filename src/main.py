import sys
import threading
import time

import mouse
import keyboard
import termcolor
import recoil_tables

from crosshair.crosshair import Crosshair
from crosshair.main import reload_crosshair
import config
import utils
from enums import *


# todo: add crosshair helper when not in ADS

class GameState:
    active_weapon = Weapons.other
    ads_active = False
    screen = Screens.play
    secondary_zoom = Zoom.x1
    active_recoil_table = None

    holding_breath = False
    is_firing = False

    fire_start_time = None

    @staticmethod
    def reset():
        GameState.active_weapon = Weapons.other
        GameState.ads = False
        GameState.screen = Screens.play
        GameState.secondary_zoom = Zoom.x1

        GameState.holding_breath = False
        GameState.is_firing = False

        GameState.fire_start_time = None
        GameState.active_recoil_table = recoil_tables.m416


class ScriptState:
    active = False

    recoil_index = 0
    last_mouse_poll_time = None
    last_keyboard_poll_time = None
    crosshair_ = None
    manual_recoil_multiplier: int = 1

    @staticmethod
    def reset():
        ScriptState.active = False
        ScriptState.recoil_index = 0
        ScriptState.last_mouse_poll_time = 0
        ScriptState.last_keyboard_poll_time = 0
        ScriptState.manual_recoil_multiplier = 1


def update_ui():
    global last_info
    script = [termcolor.colored('◼', 'red'), termcolor.colored('▶', 'green')][ScriptState.active]
    weapon = [termcolor.colored('🔫', 'green'), termcolor.colored('🔪', 'red'), termcolor.colored('💣', 'red')][GameState.active_weapon.value]
    ads    = [termcolor.colored('⚪', 'green'), termcolor.colored('⯐', 'red')][GameState.ads_active]
    screen = [termcolor.colored('🌍', 'red'), termcolor.colored('📖', 'red'), termcolor.colored('🎮', 'green')][GameState.screen.value]
    zoom2  =  termcolor.colored(f'{GameState.secondary_zoom.name[1:]}x', ['green', 'blue', 'red', 'red', 'red'][GameState.secondary_zoom.value])
    gun = termcolor.colored('m416' if GameState.active_recoil_table is recoil_tables.m416 else 'akm', 'green')
    manual_recoil = termcolor.colored(f'{ScriptState.manual_recoil_multiplier:.1f}', 'green' if ScriptState.manual_recoil_multiplier == 1 else 'red')
    breath = [termcolor.colored('👃', 'green'), termcolor.colored('👽', 'red')][GameState.holding_breath]
    firing = [termcolor.colored('😶', 'green'), termcolor.colored('⚡', 'red')][GameState.is_firing]
    recoil_index = str(ScriptState.recoil_index).zfill(3)
    sep_start = termcolor.colored('[', 'magenta')
    sep_end = termcolor.colored(']', 'magenta')
    sep_mid = termcolor.colored('] [', 'magenta')
    info = [sep_start, script, sep_mid, weapon, zoom2, ads, sep_mid, gun, manual_recoil, sep_mid, screen, firing, breath, recoil_index, sep_end]
    if info != last_info:
        sys.stdout.write('\r' + '  '.join(map(str, info)))
        sys.stdout.flush()
        last_info = info


def poll_mouse(ts):
    if ts - ScriptState.last_mouse_poll_time < config.mouse_poll_time:
        return
    ScriptState.last_mouse_poll_time = ts
    # todo: convert polls into hooks so that the wheelevent can be listened to (jumping/vaulting cancels ads)
    GameState.is_firing = (
            mouse.is_pressed('left') and
            GameState.screen == Screens.play and
            (GameState.active_weapon in [Weapons.primary, Weapons.secondary])
    )

    if GameState.is_firing:
        if GameState.fire_start_time is None:
            GameState.fire_start_time = ts
    else:
        GameState.fire_start_time = None


def poll_keyboard(ts):
    if ts - ScriptState.last_keyboard_poll_time < config.keyboard_poll_time:
        return
    ScriptState.last_keyboard_poll_time = ts
    GameState.holding_breath = keyboard.is_pressed(config.Keys.hold_breath)


def main_loop():
    while True:
        time.sleep(config.main_loop_sleep_time)

        ts = time.time()
        poll_keyboard(ts)
        poll_mouse(ts)

        update_ui()

        if not ScriptState.active or not utils.is_game_in_foreground():
            continue

        if GameState.is_firing:
            if config.enabled_anti_recoil and (ts - GameState.fire_start_time) >= ScriptState.recoil_index * config.time_between_mouse_move:
                zoom = GameState.secondary_zoom if GameState.active_weapon == Weapons.secondary and GameState.ads_active else Zoom.x1
                if zoom == Zoom.x1 and GameState.holding_breath and GameState.ads_active:
                    zoom = Zoom.xx
                amount = GameState.active_recoil_table[ScriptState.recoil_index]
                amount = int(amount * config.zoom_recoil_multipliers[zoom] * ScriptState.manual_recoil_multiplier)
                if GameState.active_weapon == Weapons.secondary:
                    amount = int(amount * 0.8)
                utils.in_game_mouse_move(amount)
                ScriptState.recoil_index = ScriptState.recoil_index + 1
                if ScriptState.recoil_index == len(GameState.active_recoil_table):
                    ScriptState.recoil_index = 0
                    mouse.release('left')
                    GameState.fire_start_time = None

            if config.enabled_limit_fire_time:
                if GameState.fire_start_time is not None and ts - GameState.fire_start_time > config.max_fire_time:
                    mouse.release('left')
        else:
            ScriptState.recoil_index = 0


def toggle_script():
    if utils.is_game_in_foreground() or config.debug:
        ScriptState.active = not ScriptState.active


def reset_state():
    ScriptState.reset()
    GameState.reset()
    cancel_ads()


def set_secondary_zoom(value: Zoom):
    if utils.is_game_in_foreground() or config.debug:
        GameState.secondary_zoom = value


def toggle_inventory():
    if utils.is_game_in_foreground() or config.debug:
        if GameState.screen == Screens.inventory:
            GameState.screen = Screens.play
        else:
            GameState.screen = Screens.inventory


def toggle_map():
    if utils.is_game_in_foreground() or config.debug:
        if GameState.screen == Screens.map:
            GameState.screen = Screens.play
        else:
            GameState.screen = Screens.map


def set_weapon_primary():
    if utils.is_game_in_foreground() or config.debug:
        GameState.active_weapon = Weapons.primary
        cancel_ads()


def set_weapon_secondary():
    if utils.is_game_in_foreground() or config.debug:
        GameState.active_weapon = Weapons.secondary
        cancel_ads()



def set_weapon_other():
    if utils.is_game_in_foreground() or config.debug:
        GameState.active_weapon = Weapons.other
        cancel_ads()


def toggle_ads():
    if utils.is_game_in_foreground() or config.debug:
        if GameState.screen == Screens.play and GameState.active_weapon in [Weapons.primary, Weapons.secondary]:
            GameState.ads_active = not GameState.ads_active
            if GameState.ads_active:
                disable_crosshair()
            else:
                enable_crosshair()


def cancel_ads():
    if utils.is_game_in_foreground() or config.debug:
        GameState.ads_active = False
        enable_crosshair()


def enable_crosshair() -> None:
    ScriptState.crosshair_ = reload_crosshair(ScriptState.crosshair_)


def disable_crosshair() -> None:
    ScriptState.crosshair_.allow_draw = False


def set_m416():
    GameState.active_recoil_table = recoil_tables.m416


def set_akm():
    GameState.active_recoil_table = recoil_tables.akm


def increase_recoil():
    ScriptState.manual_recoil_multiplier += 0.2


def decrease_recoil():
    ScriptState.manual_recoil_multiplier -= 0.2


if __name__ == '__main__':
    last_info = None

    keyboard.on_press_key(config.HotKeys.toggle_script, lambda _: toggle_script())
    keyboard.on_press_key(config.HotKeys.reset_state, lambda _: reset_state())

    keyboard.on_press_key(config.Keys.toggle_inventory, lambda _: toggle_inventory())
    keyboard.on_press_key(config.Keys.toggle_map, lambda _: toggle_map())
    mouse.on_right_click(toggle_ads)

    keyboard.on_press_key(config.HotKeys.zoom_1x, lambda _: set_secondary_zoom(Zoom.x1))
    keyboard.on_press_key(config.HotKeys.zoom_2x, lambda _: set_secondary_zoom(Zoom.x2))
    keyboard.on_press_key(config.HotKeys.zoom_3x, lambda _: set_secondary_zoom(Zoom.x3))
    keyboard.on_press_key(config.HotKeys.zoom_4x, lambda _: set_secondary_zoom(Zoom.x4))
    keyboard.on_press_key(config.HotKeys.zoom_6x, lambda _: set_secondary_zoom(Zoom.x6))

    keyboard.on_press_key(config.Keys.primary_weapon, lambda _: set_weapon_primary())
    keyboard.on_press_key(config.Keys.secondary_weapon, lambda _: set_weapon_secondary())
    keyboard.on_press_key(config.Keys.sidearm, lambda _: set_weapon_other())
    keyboard.on_press_key(config.Keys.throwables, lambda _: set_weapon_other())
    keyboard.on_press_key(config.Keys.unarm, lambda _: set_weapon_other())
    keyboard.on_press_key(config.Keys.meelee, lambda _: set_weapon_other())

    keyboard.on_press_key(config.HotKeys.m416, lambda _: set_m416())
    keyboard.on_press_key(config.HotKeys.akm, lambda _: set_akm())

    keyboard.on_press_key(config.HotKeys.recoil_increase, lambda _: increase_recoil())
    keyboard.on_press_key(config.HotKeys.recoil_decrease, lambda _: decrease_recoil())


    keyboard.on_press_key(config.Keys.reload, lambda _: cancel_ads())
    keyboard.on_press_key(config.Keys.use, lambda _: keyboard.press_and_release(config.Keys.use_redirect))


    reset_state()

    thread = threading.Thread(target=main_loop())
    thread.start()
