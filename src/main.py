import sys
import threading
import time
import typing as T

import keyboard
import mouse
import termcolor

import config
import utils
from Entitites import *
from Enums import *
from crosshair.main import reload_crosshair
from collections import Counter
import gun_detector


# todo: Detect when out of breath and cancel the effect. Can be done purely on timing with no screen reading
# todo: Convert polls into hooks so that the WheelEvent can be listened to (jumping/vaulting cancels ads)
# todo: Treat crouch and prone as a recoil multipliers
# todo: add crouch/prone detection
# todo: check if xx and zooms work differently for different guns (if yes, each gun will need a separate modifier per zoom)
# todo: control the click rate according to the guns time_between_shots for single_fire guns


class GameState:
    active_weapon: WeaponSlot
    primary_gun: Gun
    secondary_gun: Gun
    primary_zoom: Zoom
    secondary_zoom: Zoom
    screen: Screen
    ads_active: bool
    holding_breath: bool
    is_firing: bool
    fire_start_time: float

    @staticmethod
    def reset():
        GameState.active_weapon = WeaponSlots.other
        GameState.primary_gun = Guns.ump45
        GameState.secondary_gun = Guns.sniper
        GameState.primary_zoom = Zooms.x1
        GameState.secondary_zoom = Zooms.x1
        GameState.screen = Screens.play
        GameState.ads_active = False
        GameState.holding_breath = False
        GameState.is_firing = False
        GameState.fire_start_time = None


class ScriptState:
    active: bool

    recoil_compensated: T.Tuple[int, int]
    last_mouse_poll_time: float
    last_keyboard_poll_time: float
    last_screenshot_time: float
    primary_gun_votes: T.Counter[Gun]
    secondary_gun_votes: T.Counter[Gun]
    crosshair_: T.Any = None
    fire_pressed: bool
    single_fire_bullet_index: int

    @staticmethod
    def reset():
        ScriptState.active = True
        ScriptState.recoil_compensated = 0, 0
        ScriptState.last_mouse_poll_time = 0
        ScriptState.last_keyboard_poll_time = 0
        ScriptState.last_screenshot_time = 0
        ScriptState.primary_gun_votes = Counter()
        ScriptState.secondary_gun_votes = Counter()
        ScriptState.fire_pressed = False
        ScriptState.single_fire_bullet_index = 0


def screenshot(ts: float, force_update=False):
    if not force_update and ts - ScriptState.last_screenshot_time < config.time_between_screenshots:
        return
    if GameState.screen != Screens.play:
        return

    ScriptState.last_screenshot_time = ts

    if config.enabled_save_screenshot:
        ts_nano = time.perf_counter_ns()
        gun_detector.grab_and_save(label='secondary', ts_nano=ts_nano, region=config.secondary_slot_region)
        gun_detector.grab_and_save(label='primary', ts_nano=ts_nano, region=config.primary_slot_region)
    if config.enabled_gun_detection:
        if force_update:
            primary_gun = ScriptState.primary_gun_votes.most_common()[0][0]
            secondary_gun = ScriptState.secondary_gun_votes.most_common()[0][0]
            ScriptState.primary_gun_votes.clear()
            ScriptState.secondary_gun_votes.clear()
            ScriptState.primary_gun_votes[primary_gun] = 1
            ScriptState.secondary_gun_votes[secondary_gun] = 1
        primary_gun = config.gun_name_to_gun[gun_detector.grab_and_detect(region=config.primary_slot_region)]
        secondary_gun = config.gun_name_to_gun[gun_detector.grab_and_detect(region=config.secondary_slot_region)]
        ScriptState.primary_gun_votes[primary_gun] += 1
        ScriptState.secondary_gun_votes[secondary_gun] += 1
        GameState.primary_gun = ScriptState.primary_gun_votes.most_common()[0][0]
        GameState.secondary_gun = ScriptState.secondary_gun_votes.most_common()[0][0]



def update_ui():
    global last_info
    script = [termcolor.colored('◼', 'red'), termcolor.colored('▶', 'green')][ScriptState.active]
    weapon = termcolor.colored(GameState.active_weapon.symbol, ['red', 'green'][GameState.active_weapon.is_default])
    screen = termcolor.colored(GameState.screen.symbol, ['red', 'green'][GameState.screen.is_default])
    ads    = [termcolor.colored('⚪', 'green'), termcolor.colored('⯐', 'red')][GameState.ads_active]
    breath = [termcolor.colored('👃', 'green'), termcolor.colored('👽', 'red')][GameState.holding_breath]
    firing = [termcolor.colored('😶', 'green'), termcolor.colored('⚡', 'red')][GameState.is_firing]
    zoom1  =  termcolor.colored(GameState.primary_zoom.name, ['red', 'green'][GameState.primary_zoom.is_default])
    zoom2  =  termcolor.colored(GameState.secondary_zoom.name, ['red', 'green'][GameState.secondary_zoom.is_default])
    gun1 = termcolor.colored(GameState.primary_gun.name.ljust(6), 'blue' if GameState.primary_gun.safe else'red')
    gun2 = termcolor.colored(GameState.secondary_gun.name.ljust(6), 'blue' if GameState.secondary_gun.safe else'red')
    info = [[script], [weapon, ads], [gun1, zoom1], [gun2, zoom2], [screen, firing, breath]]
    if info != last_info:
        sep_beg = termcolor.colored('[', 'magenta')
        sep_end = termcolor.colored(']', 'magenta')
        sep_mid = termcolor.colored('] [', 'magenta')
        sys.stdout.write('\r' + ' '.join(utils.list_join(info, [sep_beg], [sep_mid], [sep_end])))
        sys.stdout.flush()
        last_info = info


def poll_mouse(ts):
    if ts - ScriptState.last_mouse_poll_time < config.mouse_poll_time:
        return
    ScriptState.last_mouse_poll_time = ts
    GameState.is_firing = (
            mouse.is_pressed('left') and
            GameState.screen == Screens.play
    )

    if GameState.is_firing:
        if GameState.fire_start_time is None:
            GameState.fire_start_time = ts


def poll_keyboard(ts):
    if ts - ScriptState.last_keyboard_poll_time < config.keyboard_poll_time:
        return
    ScriptState.last_keyboard_poll_time = ts
    GameState.holding_breath = keyboard.is_pressed(config.GameKeys.hold_breath)


def get_active():
    gun = {
        WeaponSlots.primary: GameState.primary_gun,
        WeaponSlots.secondary: GameState.secondary_gun,
        WeaponSlots.other: None
    }[GameState.active_weapon]
    zoom = {
        WeaponSlots.primary: GameState.primary_zoom,
        WeaponSlots.secondary: GameState.secondary_zoom,
        WeaponSlots.other: Zooms.x1
    }[GameState.active_weapon]
    if zoom == Zooms.x1 and GameState.holding_breath and GameState.ads_active:
        zoom = Zooms.x1_5
    if not GameState.ads_active:
        zoom = Zooms.x0
    return gun, zoom


def main_loop():
    while True:
        time.sleep(config.main_loop_sleep_time)

        ts = time.perf_counter()
        poll_keyboard(ts)
        poll_mouse(ts)
        screenshot(ts)

        update_ui()

        if not ScriptState.active or not utils.is_game_in_foreground():
            continue

        gun, zoom = get_active()
        multiplier = zoom.recoil_multiplier
        ts = time.perf_counter()

        if GameState.is_firing and GameState.fire_start_time is not None and GameState.active_weapon in [WeaponSlots.primary, WeaponSlots.secondary]:
            dt = ts - GameState.fire_start_time
            if gun.type_ == GunTypes.single_fire:
                if ScriptState.single_fire_bullet_index * gun.time_between_shots < dt:
                    keyboard.press_and_release(GameKeys.fire)
                    ScriptState.single_fire_bullet_index += 1
            elif gun.type_ == GunTypes.full_auto and not ScriptState.fire_pressed:
                keyboard.press(GameKeys.fire)
                ScriptState.fire_pressed = True
            elif gun.type_ == GunTypes.bolt_action and not ScriptState.fire_pressed:
                keyboard.press(GameKeys.fire)
                ScriptState.fire_pressed = True

            x_moved, y_moved = ScriptState.recoil_compensated
            dx, dy = gun.get_mouse_move_amount(time_since_fire_start=dt, x_moved=x_moved, y_moved=y_moved, multiplier=multiplier)

            if config.enabled_anti_recoil and dt >= config.time_between_mouse_move:
                if dx != 0 or dy > 0:
                    utils.in_game_mouse_move(dx, dy)
                    ScriptState.recoil_compensated = x_moved + dx, y_moved + dy

            if gun.get_bullets_fired(dt) == min(config.bullet_limit, len(gun.vertical_recoil)):
                mouse.release('left')
                GameState.fire_start_time = None
                ScriptState.recoil_compensated = 0, 0
        elif GameState.is_firing and GameState.active_weapon == WeaponSlots.other:
            if not ScriptState.fire_pressed:
                keyboard.press(GameKeys.fire)
                ScriptState.fire_pressed = True
        else:
            if ScriptState.fire_pressed:
                keyboard.release(GameKeys.fire)
                ScriptState.fire_pressed = False
            if GameState.fire_start_time is not None:
                if config.enabled_anti_recoil and gun is not None:
                    last_vertical_recoil = gun.vertical_recoil[ScriptState.single_fire_bullet_index]
                    readjust_amount = - int(last_vertical_recoil / 0.7)
                    utils.in_game_mouse_move(0, readjust_amount)
                GameState.fire_start_time = None
            ScriptState.recoil_compensated = 0, 0
            ScriptState.single_fire_bullet_index = 0


def toggle_script():
    if utils.is_game_in_foreground() or config.debug:
        ScriptState.active = not ScriptState.active


def reset_state():
    ScriptState.reset()
    GameState.reset()
    cancel_ads()
    keyboard.release(GameKeys.fire)


def set_zoom(value: Zoom):
    if utils.is_game_in_foreground() or config.debug:
        if GameState.active_weapon == WeaponSlots.primary:
            GameState.primary_zoom = value
        elif GameState.active_weapon == WeaponSlots.secondary:
            GameState.secondary_zoom = value


def toggle_inventory():
    if utils.is_game_in_foreground() or config.debug:
        if GameState.screen == Screens.inventory:
            GameState.screen = Screens.play
            screenshot(time.perf_counter(), force_update=True)
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
        GameState.active_weapon = WeaponSlots.primary
        cancel_ads()
        enable_crosshair()


def set_weapon_secondary():
    if utils.is_game_in_foreground() or config.debug:
        GameState.active_weapon = WeaponSlots.secondary
        cancel_ads()
        enable_crosshair()



def set_weapon_other():
    if utils.is_game_in_foreground() or config.debug:
        GameState.active_weapon = WeaponSlots.other
        cancel_ads()
        disable_crosshair()


def toggle_ads():
    if utils.is_game_in_foreground() or config.debug:
        if GameState.screen == Screens.play and GameState.active_weapon in [WeaponSlots.primary, WeaponSlots.secondary]:
            GameState.ads_active = not GameState.ads_active
            if GameState.ads_active:
                disable_crosshair()
            else:
                enable_crosshair()


def cancel_ads():
    if utils.is_game_in_foreground() or config.debug:
        GameState.ads_active = False
        if GameState.active_weapon in [WeaponSlots.primary, WeaponSlots.secondary]:
            enable_crosshair()


def enable_crosshair() -> None:
    if config.enabled_crosshair:
        ScriptState.crosshair_ = reload_crosshair(ScriptState.crosshair_)


def disable_crosshair() -> None:
    if config.enabled_crosshair and ScriptState.crosshair_ is not None:
        ScriptState.crosshair_.allow_draw = False


def cycle_gun(gun: Gun, direction: int) -> Gun:
    index = config.guns_sorted_by_recoil.index(gun)
    index = (index + direction) % len(config.guns_sorted_by_recoil)
    return config.guns_sorted_by_recoil[index]


def increase_recoil():
    if utils.is_game_in_foreground() or config.debug:
        if GameState.active_weapon == WeaponSlots.primary:
            GameState.primary_gun = cycle_gun(GameState.primary_gun, 1)
        elif GameState.active_weapon == WeaponSlots.secondary:
            GameState.secondary_gun = cycle_gun(GameState.secondary_gun, 1)


def decrease_recoil():
    if utils.is_game_in_foreground() or config.debug:
        if GameState.active_weapon == WeaponSlots.primary:
            GameState.primary_gun = cycle_gun(GameState.primary_gun, -1)
        elif GameState.active_weapon == WeaponSlots.secondary:
            GameState.secondary_gun = cycle_gun(GameState.secondary_gun, -1)


def interact_pressed():
    keyboard.press_and_release(config.GameKeys.use_redirect)
    screenshot(time.perf_counter(), force_update=True)


if __name__ == '__main__':
    last_info = None

    keyboard.on_press_key(config.HotKeys.toggle_script, lambda _: toggle_script())
    keyboard.on_press_key(config.HotKeys.reset_state, lambda _: reset_state())

    keyboard.on_press_key(config.GameKeys.toggle_inventory, lambda _: toggle_inventory())
    keyboard.on_press_key(config.GameKeys.toggle_map, lambda _: toggle_map())
    mouse.on_right_click(toggle_ads)

    keyboard.on_press_key(config.HotKeys.zoom_1x, lambda _: set_zoom(Zooms.x1))
    keyboard.on_press_key(config.HotKeys.zoom_2x, lambda _: set_zoom(Zooms.x2))
    keyboard.on_press_key(config.HotKeys.zoom_3x, lambda _: set_zoom(Zooms.x3))
    keyboard.on_press_key(config.HotKeys.zoom_4x, lambda _: set_zoom(Zooms.x4))
    keyboard.on_press_key(config.HotKeys.zoom_6x, lambda _: set_zoom(Zooms.x6))

    keyboard.on_press_key(config.GameKeys.primary_weapon, lambda _: set_weapon_primary())
    keyboard.on_press_key(config.GameKeys.secondary_weapon, lambda _: set_weapon_secondary())
    keyboard.on_press_key(config.GameKeys.sidearm, lambda _: set_weapon_other())
    keyboard.on_press_key(config.GameKeys.throwables, lambda _: set_weapon_other())
    keyboard.on_press_key(config.GameKeys.unarm, lambda _: set_weapon_other())
    keyboard.on_press_key(config.GameKeys.melee, lambda _: set_weapon_other())

    keyboard.on_press_key(config.HotKeys.recoil_increase, lambda _: increase_recoil())
    keyboard.on_press_key(config.HotKeys.recoil_decrease, lambda _: decrease_recoil())


    keyboard.on_press_key(config.GameKeys.reload, lambda _: cancel_ads())
    keyboard.on_press_key(config.GameKeys.use, lambda _: interact_pressed())


    reset_state()

    thread = threading.Thread(target=main_loop())
    thread.start()
