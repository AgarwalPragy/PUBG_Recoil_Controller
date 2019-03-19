from enum import IntEnum
from enums import *

__all__ = ['mouse_poll_time', 'time_between_mouse_move', 'recoil_table', 'recoil_multipliers', 'Keys', 'HotKeys']

debug = False

enabled_anti_recoil = True
enabled_ads_help = False
# todo: ads helper really screws us over by turning on hip fire,
#  or removing our ads, and the costs outweigh the benefits.
#  It can be improved by detecting when we've been in ads
#  for too long while moving or doing ads cancelling things.
enabled_lean_help = False
# todo: can be improved by detecting when an
#  ads while previously active, and not changing the ads direction once set
#  Currently, trying to get back to cover while firing while learning
#  right, will cause the lean to shift to left which screws stuff up.


enabled_limit_fire_time = False

main_loop_sleep_time = 0.01
mouse_poll_time = 0.01
time_between_mouse_move = 0.02
keyboard_poll_time = 0.05
movement_direction_decay_time = 0.3
max_fire_time = 1
burst_time = 0.3

max_info_lines = 3

recoil_table = [  # optimized for m416
    6, 6, 6, 6, 4,
    3, 3, 3, 4, 4,
    3, 3, 3, 4, 4,
    3, 3, 4, 4, 4,
    4, 4, 4, 5, 5,
    5, 5, 5, 5, 5,
    5, 5, 5, 5, 5,  # 07 bullets

    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,  # 14 bullets

    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,  # 21 bullets

    5, 5, 5, 6, 6,
    5, 5, 5, 6, 6,
    5, 5, 5, 6, 6,
    5, 5, 5, 6, 6,
    5, 5, 5, 6, 6,
    5, 5, 5, 6, 6,
    5, 5, 5, 6, 6,  # 28 bullets

    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,  # 35 bullets

    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,
    5, 5, 5, 5, 6,  # 40 bullets

]

recoil_multipliers = {
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

    hold_breath      = 42  # left shift
    toggle_canted    = 59  # F1
    alternate_ads    = 60  # F2
    alternate_fire   = 61  # F1


    toggle_map       = 33  # f
    toggle_inventory = 15  # tab

    reload           = 19  # r


class HotKeys(IntEnum):
    rotate_primary_zoom   = 12  # -
    rotate_secondary_zoom = 13  # =
    toggle_script         = 41  # `
    reset_state           = 1   # esc


game_window_text = "PLAYERUNKNOWN'S BATTLEGROUNDS "
