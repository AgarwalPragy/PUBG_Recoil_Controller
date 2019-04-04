from enum import IntEnum
from enums import *

__all__ = ['mouse_poll_time', 'time_between_mouse_move', 'zoom_recoil_multipliers', 'Keys', 'HotKeys']

# =========================================
# toggles
# =========================================

debug = False
enabled_anti_recoil = True
enabled_limit_fire_time = False

# =========================================
# timings
# =========================================

max_fire_time = 1
main_loop_sleep_time = 0.01
mouse_poll_time = 0.01
time_between_mouse_move = 0.02
keyboard_poll_time = 0.05
burst_time = 0.3

# =========================================
# output
# =========================================

max_info_lines = 3


# =========================================
# recoil
# =========================================

zoom_recoil_multipliers = {
    Zoom.x1: 1,
    Zoom.x2: 1.8,
    Zoom.x3: 2.65,
    Zoom.x4: 3.6,
    Zoom.x6: 5.2,
    Zoom.xx: 1.4,
    # todo: detect when out of breath and cancel the effect
    #  can be done purely on timing with no screen reading

    # todo: add logic for quick tapping
    #  currently, the initial high recoil control
    #  pulls the mouse down too much while tapping.
}

# =========================================
# Bindings
# =========================================


class Keys(IntEnum):
    primary_weapon   = 2   # key num 1
    secondary_weapon = 3   # key num 2
    sidearm          = 4   # key num 3

    throwables       = 5   # key num 4
    meelee           = 44  # z
    unarm            = 45  # x

    use              = 102  # F15
    use_redirect     = 25   # p
    reload           = 19   # r

    toggle_map       = 33  # f
    toggle_inventory = 15  # tab

    lean_left        = 16  # q
    lean_right       = 18  # e
    strafe_left      = 30  # a
    strafe_right     = 32  # d

    hold_breath      = 42  # left shift

    alternate_ads    = 68  # F10
    alternate_fire   = 87  # F11


class HotKeys(IntEnum):
    zoom_1x          = 59  # F1
    zoom_2x          = 60  # F2
    zoom_3x          = 61  # F3
    zoom_4x          = 62  # F4
    zoom_6x          = 64  # F6

    m416             = 100  # F13
    akm              = 101  # F14
    recoil_increase  = 104  # F17
    recoil_decrease  = 105  # F18

    toggle_script    = 41  # `
    reset_state      = 1   # esc

# =========================================
# others
# =========================================


game_window_text = "PLAYERUNKNOWN'S BATTLEGROUNDS "
