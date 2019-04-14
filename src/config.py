from Entitites import *
from Enums import *

__all__ = [
    'debug', 'enabled_anti_recoil', 'enabled_crosshair',
    'main_loop_sleep_time', 'mouse_poll_time', 'keyboard_poll_time', 'time_between_mouse_move',
    'game_window_text', 'max_info_lines',
    'bullet_limit',
]

# =============================================================================================
#  Toggles

debug: bool = False
enabled_anti_recoil: bool = True
enabled_crosshair: bool = True
enabled_save_screenshot: bool = False
enabled_gun_detection: bool = True

# =============================================================================================
#  Timings

main_loop_sleep_time: float = 0.01
mouse_poll_time: float = 0.01
keyboard_poll_time: float = 0.05
time_between_mouse_move: float = 0.01
time_between_screenshots: float = 1.0

# =============================================================================================
#  Others

game_window_text: str = "PLAYERUNKNOWN'S BATTLEGROUNDS "
max_info_lines: int = 3
secondary_slot_region = 1442, 949, 1596, 993
primary_slot_region = 1442, 1008, 1596, 1052

# =============================================================================================
#  Bindings

GameKeys.primary_weapon   =   2  # 1
GameKeys.secondary_weapon =   3  # 2
GameKeys.sidearm          =   4  # 3
GameKeys.throwables       =   5  # 4
GameKeys.melee            =  44  # z
GameKeys.unarm            =  45  # x

GameKeys.use              = 102  # F15
GameKeys.use_redirect     =  25  # p
GameKeys.reload           =  19  # r
GameKeys.toggle_map       =  33  # f
GameKeys.toggle_inventory =  15  # tab

GameKeys.lean_left        =  16  # q
GameKeys.lean_right       =  18  # e
GameKeys.strafe_left      =  30  # a
GameKeys.strafe_right     =  32  # d

GameKeys.hold_breath      =  42  # left shift

GameKeys.alternate_ads    =  68  # F10
GameKeys.alternate_fire   =  87  # F11

HotKeys.zoom_1x           =  59  # F1
HotKeys.zoom_2x           =  60  # F2
HotKeys.zoom_3x           =  61  # F3
HotKeys.zoom_4x           =  62  # F4
HotKeys.zoom_6x           =  64  # F6

HotKeys.m416              = 104  # F17
HotKeys.akm               = 105  # F18
HotKeys.recoil_increase   = 100  # F13
HotKeys.recoil_decrease   = 101  # F14

HotKeys.toggle_script     =  41  # `
HotKeys.reset_state       =   1  # esc

# =============================================================================================
#  Zooms

Zooms.x1.recoil_multiplier = 1.0
Zooms.x2.recoil_multiplier = 1.9
Zooms.x3.recoil_multiplier = 2.85
Zooms.x4.recoil_multiplier = 3.95
Zooms.x6.recoil_multiplier = 5.55
Zooms.xx.recoil_multiplier = 1.3


# =============================================================================================
#  Guns

Guns.m416 = Gun(
    name='m416',
    time_between_shots=0.102,
    vertical_recoil=[
        22, 22, 22, 24, 25,
        30, 30, 32, 32, 32,
        32, 32, 32, 32, 32,
        32, 32, 32, 32, 32,
        32, 34, 34, 34, 34,
        34, 34, 34, 32, 32,
        32, 32, 32, 32, 32,
        32, 32, 32, 32, 32,
    ],
    horizontal_recoil=[
        0, 0, 1, 1, 1,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
    ],
)

Guns.akm = Gun(
    name='akm',
    time_between_shots=0.1,
    vertical_recoil=[
        18, 29, 29, 29, 29,
        40, 40, 40, 46, 46,
        46, 46, 50, 50, 50,
        50, 50, 52, 52, 52,
        52, 52, 52, 53, 53,
        53, 53, 53, 53, 53,
        53, 53, 53, 53, 53,
        53, 53, 53, 53, 53,
    ],
    horizontal_recoil=[
        0, 0, 0, 0, 0,
        0, 1, 0, 1, 0,
        1, 0, 1, 0, 1,
        0, 1, 0, 1, 0,
        1, 0, 1, 0, 1,
        0, 1, 0, 1, 0,
        1, 0, 1, 0, 1,
        0, 1, 0, 1, 0,
    ],
)

Guns.uzi = Gun(
    name='uzi',
    time_between_shots=0.051,
    vertical_recoil=[
         5,  6, 10, 10, 13,
        15, 15, 18, 20, 20,
        23, 23, 23, 23, 23,
        27, 27, 27, 27, 27,
        32, 32, 32, 32, 32,
        32, 32, 32, 32, 32,
        32, 32, 32, 32, 32
    ],
    horizontal_recoil=[
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
    ],
)

Guns.bizon = Gun(
    name='bizon',
    time_between_shots=0.102,
    vertical_recoil=[
        10, 10, 15, 18, 18,
        20, 24, 24, 24, 24,
        24, 24, 24, 24, 24,
        24, 24, 24, 24, 24,
        22, 22, 22, 22, 22,
        22, 22, 22, 22, 22,
        22, 22, 22, 22, 22,
        23, 23, 23, 23, 23,
        23, 23, 23, 23, 23,
        23, 23, 23, 23, 23,
        23, 23, 23,
    ],
    horizontal_recoil=[
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 1, 0, 1, 0,
        1, 0, 1, 0, 1,
        0, 1, 0, 1, 0,
        1, 0, 1, 0, 1,
        1, 0, 1, 0, 1,
        0, 1, 0, 1, 0,
        1, 0, 1, 0, 1,
        0, 1, 0, 1, 0,
        1, 0, 1,
    ],
)

Guns.vector = Gun(
    name='vector',
    time_between_shots=0.068,
    vertical_recoil=[
        10, 10, 13, 16, 16,
        18, 22, 23, 23, 23,
        24, 24, 24, 25, 25,
        25, 25, 25, 26, 26,
        26, 26, 26, 28, 28,
        28, 28, 30, 30, 30,
        32, 32, 32,
    ],
    horizontal_recoil=[
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 1, 0, 1, 0,
        1, 0, 1, 0, 1,
        0, 1, 0, 1, 0,
        1, 0, 1, 0, 1,
        1, 0, 1,
    ],
)

Guns.g36c = Gun(
    name='g36c',
    time_between_shots=0.102,
    vertical_recoil=[
        17, 17, 17, 20, 20,
        29, 29, 31, 31, 31,
        31, 31, 31, 31, 31,
        31, 31, 31, 31, 31,
        31, 33, 33, 33, 33,
        33, 33, 33, 31, 31,
        31, 31, 31, 31, 31,
        31, 31, 31, 31, 31,
    ],
    horizontal_recoil=[
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
    ],
)

Guns.ump45 = Gun(
    name='ump45',
    time_between_shots=0.102,
    vertical_recoil=[
        12, 12, 17, 22, 22,
        24, 26, 26, 26, 26,
        26, 26, 27, 28, 28,
        30, 30, 30, 30, 30,
        30, 30, 30, 30, 30,
        30, 30, 30, 30, 30,
        30, 30, 30, 30, 30,
    ],
    horizontal_recoil=[
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
    ],
)

Guns.sniper = Gun(
    name='sniper',
    time_between_shots=1,
    vertical_recoil=[0]*100,
    horizontal_recoil=[0]*100,
)

Guns.apple = Gun.copy_from(Guns.sniper, 'apple')
Guns.hegrenade = Gun.copy_from(Guns.sniper, 'hegrenade')
Guns.molotov = Gun.copy_from(Guns.sniper, 'molotov')
Guns.skorpion = Gun.copy_from(Guns.sniper, 'skorpion')

Guns.awm = Gun.copy_from(Guns.sniper, 'awm')
Guns.kar98k = Gun.copy_from(Guns.sniper, 'kar98k')
Guns.m24 = Gun.copy_from(Guns.sniper, 'm24')
Guns.crossbow = Gun.copy_from(Guns.sniper, 'crossbow')

Guns.mini14 = Gun.copy_from(Guns.sniper, 'mini14')
Guns.qbu = Gun.copy_from(Guns.sniper, 'qbu')
Guns.sks = Gun.copy_from(Guns.sniper, 'sks')
Guns.slr = Gun.copy_from(Guns.sniper, 'slr')
Guns.vss = Gun.copy_from(Guns.sniper, 'vss')

Guns.m16a4 = Gun.copy_from(Guns.sniper, 'm16a4')
Guns.s12k = Gun.copy_from(Guns.sniper, 's12k')
Guns.mutant = Gun.copy_from(Guns.sniper, 'mutant')
Guns.s686 = Gun.copy_from(Guns.sniper, 's686')
Guns.s1897 = Gun.copy_from(Guns.sniper, 's1897')


Guns.aug = Gun.copy_from(Guns.m416, 'aug')
Guns.beryl = Gun.copy_from(Guns.akm, 'beryl')
Guns.dp28 = Gun.copy_from(Guns.akm, 'dp28')
Guns.groza = Gun.copy_from(Guns.akm, 'groza')
Guns.m249 = Gun.copy_from(Guns.akm, 'm249')
Guns.mk14 = Gun.copy_from(Guns.akm, 'mk14')
Guns.mp5k = Gun.copy_from(Guns.ump45, 'mp5k')
Guns.qbz = Gun.copy_from(Guns.m416, 'qbz')
Guns.scarl = Gun.copy_from(Guns.m416, 'scarl')
Guns.tommy = Gun.copy_from(Guns.ump45, 'tommy')


guns_sorted_by_recoil = sorted([gun for gun in Guns.__dict__.values() if isinstance(gun, Gun)], key=lambda x: x.recoil_per_second)
gun_name_to_gun = {gun.name: gun for gun in Guns.__dict__.values() if isinstance(gun, Gun)}
bullet_limit = 53
