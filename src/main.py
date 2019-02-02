import sys
import threading
import time

import mouse
import keyboard
import termcolor

import config
import utils
from enums import *


class GameState:
    active_weapon = Weapons.other
    canted_active = False
    ads_active = False
    screen = Screens.play
    primary_zoom = Zoom.x1

    holding_breath = False
    is_firing = False

    fire_start_time = None
    applicable_strafe_direction = None

    @staticmethod
    def reset():
        GameState.active_weapon = Weapons.other
        GameState.canted_active = False
        GameState.ads = False
        GameState.screen = Screens.play
        GameState.primary_zoom = Zoom.x1

        GameState.holding_breath = False
        GameState.is_firing = False

        GameState.fire_start_time = None
        GameState.applicable_strafe_direction = None


class ScriptState:
    active = False

    last_strafe_direction_time = None
    recoil_index = 0

    ads_helping = False
    lean_helping = False

    last_mouse_poll_time = None
    last_keyboard_poll_time = None

    @staticmethod
    def reset():
        ScriptState.active = False

        ScriptState.last_strafe_direction_time = 0
        ScriptState.recoil_index = 0

        ScriptState.ads_helping = False
        ScriptState.lean_helping = False

        ScriptState.last_mouse_poll_time = 0
        ScriptState.last_keyboard_poll_time = 0


def update_ui():
    global last_info
    script = [termcolor.colored('◼', 'red'), termcolor.colored('▶', 'green')][ScriptState.active]
    weapon = [termcolor.colored('🔫', 'green'), termcolor.colored('🔪', 'red'), termcolor.colored('💣', 'red')][GameState.active_weapon.value]
    canted = [termcolor.colored('⦻', 'green'), termcolor.colored('⛶', 'red')][GameState.canted_active]
    ads    = [termcolor.colored('⚪', 'green'), termcolor.colored('⯐', 'red')][GameState.ads_active]
    screen = [termcolor.colored('🌍', 'red'), termcolor.colored('📖', 'red'), termcolor.colored('🎮', 'green')][GameState.screen.value]
    zoom1  =  termcolor.colored(f'{GameState.primary_zoom.name[1:]}x', ['green', 'blue', 'red', 'red', 'red'][GameState.primary_zoom.value])
    breath = [termcolor.colored('👃', 'green'), termcolor.colored('👽', 'red')][GameState.holding_breath]
    firing = [termcolor.colored('😶', 'green'), termcolor.colored('⚡', 'red')][GameState.is_firing]
    strafe = termcolor.colored('⊙', 'green') if GameState.applicable_strafe_direction is None else termcolor.colored(['⇦', '⇨'][GameState.applicable_strafe_direction.value], 'red')
    recoil_index = str(ScriptState.recoil_index).zfill(3)
    sep_start = termcolor.colored('[', 'magenta')
    sep_end = termcolor.colored(']', 'magenta')
    sep_mid = termcolor.colored('] [', 'magenta')
    info = [sep_start, script, sep_mid, weapon, zoom1, canted, ads, sep_mid, screen, firing, strafe, breath, recoil_index, sep_end]
    if info != last_info:
        sys.stdout.write('\r' + '  '.join(map(str, info)))
        sys.stdout.flush()
        last_info = info


def poll_mouse(ts):
    if ts - ScriptState.last_mouse_poll_time < config.mouse_poll_time:
        return
    ScriptState.last_mouse_poll_time = ts

    GameState.is_firing = (
            mouse.is_pressed('left') and
            GameState.screen == Screens.play and
            (GameState.active_weapon == Weapons.primary)
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

    if keyboard.is_pressed(config.Keys.strafe_right):
        GameState.applicable_strafe_direction = Movement.right
        ScriptState.last_strafe_direction_time = ts
    elif keyboard.is_pressed(config.Keys.strafe_left):
        GameState.applicable_strafe_direction = Movement.left
        ScriptState.last_strafe_direction_time = ts
    elif ts - ScriptState.last_strafe_direction_time > config.movement_direction_decay_time:
        GameState.applicable_strafe_direction = None

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
            if config.enabled_ads_help:
                if not GameState.ads_active and not ScriptState.ads_helping:
                    keyboard.press_and_release(config.Keys.ads)
                    GameState.canted_active = True
                    ScriptState.ads_helping = True
                    GameState.ads_active = True
                    keyboard.press_and_release(config.Keys.toggle_canted)
            if config.enabled_anti_recoil and (ts - GameState.fire_start_time) >= ScriptState.recoil_index * config.time_between_mouse_move:
                zoom = Zoom.x1 if GameState.canted_active else GameState.primary_zoom
                if zoom == Zoom.x1 and GameState.holding_breath:
                    zoom = Zoom.xx
                amount = config.recoil_table[ScriptState.recoil_index]
                amount = int(amount * config.recoil_multipliers[zoom])
                utils.in_game_mouse_move(amount)
                ScriptState.recoil_index = ScriptState.recoil_index + 1
                if ScriptState.recoil_index == len(config.recoil_table):
                    ScriptState.recoil_index = 0
                    mouse.release('left')
                    GameState.fire_start_time = None


            if config.enabled_lean_help:
                if GameState.applicable_strafe_direction == Movement.left and not ScriptState.lean_helping:
                    keyboard.press(config.Keys.lean_left)
                    ScriptState.lean_helping = True
                elif GameState.applicable_strafe_direction is Movement.right and not ScriptState.lean_helping:
                    keyboard.press(config.Keys.lean_right)
                    ScriptState.lean_helping = True
                else:
                    # don't touch anything. We might have gone from strafing to leaned firing which caused the application direction
                    # to vanish or change, so if we're already in a lean, we shouldn't cancel or change directions.
                    pass

            if config.enabled_limit_fire_time:
                if GameState.fire_start_time is not None and ts - GameState.fire_start_time > config.max_fire_time:
                    mouse.release('left')
        else:
            if ScriptState.ads_helping:
                keyboard.press_and_release(config.Keys.toggle_canted)
                ScriptState.ads_helping = False
                GameState.ads_active = False
                GameState.canted_active = False
                keyboard.press_and_release(config.Keys.ads)
            if ScriptState.lean_helping:
                keyboard.release(config.Keys.lean_left)
                keyboard.release(config.Keys.lean_right)
                ScriptState.lean_helping = False

            ScriptState.recoil_index = 0


def toggle_script():
    if utils.is_game_in_foreground() or config.debug:
        ScriptState.active = not ScriptState.active


def reset_state():
    ScriptState.reset()
    GameState.reset()


def rotate_primary_zoom():
    if utils.is_game_in_foreground() or config.debug:
        GameState.primary_zoom = Zoom((GameState.primary_zoom.value + 1) % 5)


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


def set_weapon_secondary():
    if utils.is_game_in_foreground() or config.debug:
        GameState.active_weapon = Weapons.secondary


def set_weapon_other():
    if utils.is_game_in_foreground() or config.debug:
        GameState.active_weapon = Weapons.other


def toggle_ads():
    if utils.is_game_in_foreground() or config.debug:
        if GameState.screen == Screens.play and GameState.active_weapon == Weapons.primary:
            GameState.ads_active = not GameState.ads_active


def cancel_ads():
    if utils.is_game_in_foreground() or config.debug:
        GameState.ads_active = False


if __name__ == '__main__':
    last_info = None

    keyboard.on_press_key(config.HotKeys.toggle_script, lambda _: toggle_script())
    keyboard.on_press_key(config.HotKeys.reset_state, lambda _: reset_state())

    keyboard.on_press_key(config.Keys.toggle_inventory, lambda _: toggle_inventory())
    keyboard.on_press_key(config.Keys.toggle_map, lambda _: toggle_map())

    keyboard.on_press_key(config.HotKeys.rotate_primary_zoom, lambda _: rotate_primary_zoom())

    keyboard.on_press_key(config.Keys.primary_weapon, lambda _: set_weapon_primary())
    mouse.on_right_click(toggle_ads)
    keyboard.on_press_key(config.Keys.secondary_weapon, lambda _: set_weapon_secondary())
    keyboard.on_press_key(config.Keys.sidearm, lambda _: set_weapon_other())
    keyboard.on_press_key(config.Keys.throwables, lambda _: set_weapon_other())
    keyboard.on_press_key(config.Keys.unarm, lambda _: set_weapon_other())
    keyboard.on_press_key(config.Keys.he_grenade, lambda _: set_weapon_other())
    keyboard.on_press_key(config.Keys.stun_grenade, lambda _: set_weapon_other())
    keyboard.on_press_key(config.Keys.molotov, lambda _: set_weapon_other())
    keyboard.on_press_key(config.Keys.smoke_grenade, lambda _: set_weapon_other())
    keyboard.on_press_key(config.Keys.reload, lambda _: cancel_ads())

    reset_state()

    thread = threading.Thread(target=main_loop())
    thread.start()
