from enum import IntEnum
from enums import *

__all__ = ['mouse_poll_time', 'time_between_mouse_move', 'recoil_table', 'recoil_multipliers', 'Keys', 'HotKeys']

debug = False

enabled_anti_recoil = True
enabled_ads_help = True
enabled_lean_help = True
enabled_limit_fire_time = False

main_loop_sleep_time = 0.01
mouse_poll_time = 0.01
time_between_mouse_move = 0.02
keyboard_poll_time = 0.05
movement_direction_decay_time = 0.3
max_fire_time = 1
burst_time = 0.3

max_info_lines = 3

recoil_table = [
    4, 5, 4, 5, 4, 4, 5, 4, 5, 4,
    4, 5, 4, 5, 4, 4, 5, 4, 5, 4,
    4, 5, 4, 5, 4, 4, 5, 4, 5, 4,
    4, 5, 4, 5, 4, 4, 5, 4, 5, 4,
    6, 6, 6, 6, 6, 6, 6, 6, 6, 7,
    7, 7, 7, 7, 6, 6, 6, 6, 6, 6,
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 9, 9, 8, 8,
    9, 9, 9, 9, 9, 9, 9, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    9, 9,
]

recoil_multipliers = {
    Zoom.x1: 1,
    Zoom.x2: 1.8,
    Zoom.x3: 2.3,
    Zoom.x4: 3.7,
    Zoom.x6: 5.3,
    Zoom.xx: 1.4,
}


class Keys(IntEnum):
    primary_weapon   = 2   # key num 1
    secondary_weapon = 3   # key num 2
    sidearm          = 4   # key num 3
    molotov          = 6   # key num 5
    smoke_grenade    = 8   # key num 7
    he_grenade       = 9   # key num 8
    stun_grenade     = 10  # key num 9

    throwables       = 34  # g
    unarm            = 45  # x
    use              = 7   # key num 6

    lean_left        = 16  # q
    lean_right       = 18  # e
    strafe_left      = 30  # a
    strafe_right     = 32  # d

    ads              = 14  # backspace
    hold_breath      = 42  # left shift
    toggle_canted    = 59  # F1

    toggle_map       = 33  # f
    toggle_inventory = 15  # tab

    reload           = 19  # r


class HotKeys(IntEnum):
    rotate_primary_zoom   = 12  # -
    rotate_secondary_zoom = 13  # =
    toggle_script         = 41  # `
    reset_state           = 1   # esc


game_window_text = "PLAYERUNKNOWN'S BATTLEGROUNDS "
