from Entitites import *

__all__ = ['Screens', 'WeaponSlots', 'Zooms', 'GameKeys', 'HotKeys', 'Guns']


class Screens:
    play = Screen('Play', True, '🎮')
    map = Screen('Map', False, '🌍')
    inventory = Screen('Inventory', False, '📖')


class WeaponSlots:
    primary = WeaponSlot('Primary', True, '🔫')
    secondary = WeaponSlot('Secondary', False, '🔪')
    other = WeaponSlot('Other', False, '💣')


class Zooms:
    x1 = Zoom('1×', True)
    x2 = Zoom('2×', False)
    x3 = Zoom('3×', False)
    x4 = Zoom('4×', False)
    x6 = Zoom('6×', False)
    xx = Zoom('××', False)


class GameKeys:
    alternate_ads: int
    alternate_fire: int
    hold_breath: int
    lean_left: int
    lean_right: int
    melee: int
    primary_weapon: int
    reload: int
    secondary_weapon: int
    sidearm: int
    strafe_left: int
    strafe_right: int
    throwables: int
    toggle_inventory: int
    toggle_map: int
    unarm: int
    use: int
    use_redirect: int


class HotKeys:
    recoil_decrease: int
    recoil_increase: int
    reset_state: int
    toggle_script: int
    zoom_1x: int
    zoom_2x: int
    zoom_3x: int
    zoom_4x: int
    zoom_6x: int
    m416: int
    akm: int


class Guns:
    m416: Gun
    akm: Gun
    uzi: Gun
    bizon: Gun
    vector: Gun
    sniper: Gun
    g36c: Gun
    ump45: Gun

