import typing as T
from Entitites import *
from Enums import *
import config_guns

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
GameKeys.fire             =  66  # F8

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

Zooms.x0.recoil_multiplier = 0.85
Zooms.x1.recoil_multiplier = 1.0
Zooms.x1_5.recoil_multiplier = 1.35
Zooms.x2.recoil_multiplier = 1.8
Zooms.x3.recoil_multiplier = 2.75
Zooms.x4.recoil_multiplier = 3.8
Zooms.x6.recoil_multiplier = 5.5

# =============================================================================================
#  Guns

bullet_limit: int = 53

guns_sorted_by_recoil: T.List[Gun] = sorted([gun for gun in Guns.__dict__.values() if isinstance(gun, Gun)], key=lambda x: x.recoil_per_second)
gun_name_to_gun: T.Dict[str, Gun] = {gun.name: gun for gun in Guns.__dict__.values() if isinstance(gun, Gun)}
for gun in guns_sorted_by_recoil:
    assert len(gun.horizontal_recoil) == len(gun.vertical_recoil), gun.name


# =============================================================================================
#  Others

# Brightness / Contrast
#     Exposure: 0
#     Contrast: 50
#     Highlights: -70
#     Shadows: -100
#     Gamma: 20
# Details
#     Sharpen: 26
#     Clarity: 22
#     HDR Toning: 70
#     Bloom: 0
# Colour
#     Tint Intensity: 0
#     Temperature: 0
#     Vibrance: 10

game_window_text: str = "PLAYERUNKNOWN'S BATTLEGROUNDS "
max_info_lines: int = 3
secondary_slot_region = 1442, 949, 1596, 993
primary_slot_region = 1442, 1008, 1596, 1052
