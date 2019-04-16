from Entitites import *

__all__ = ['Screens', 'WeaponSlots', 'Zooms', 'GameKeys', 'HotKeys', 'Guns', 'GunTypes']


class Screens:
    play = Screen('Play', True, '🎮')
    map = Screen('Map', False, '🌍')
    inventory = Screen('Inventory', False, '📖')


class WeaponSlots:
    primary = WeaponSlot('Primary', True, '🔫')
    secondary = WeaponSlot('Secondary', False, '🔪')
    other = WeaponSlot('Other', False, '💣')


class Zooms:
    x0 = Zoom('0x', False)
    x1 = Zoom('1×', True)
    x1_5 = Zoom('1.5x', False)
    x2 = Zoom('2×', False)
    x3 = Zoom('3×', False)
    x4 = Zoom('4×', False)
    x6 = Zoom('6×', False)



class GameKeys:
    alternate_ads: int
    fire: int
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


class GunTypes:
    full_auto = GunType(0)
    single_fire = GunType(1)
    bolt_action = GunType(2)


class Guns:
    m416: Gun
    akm: Gun
    uzi: Gun
    bizon: Gun
    vector: Gun
    sniper: Gun
    g36c: Gun
    ump45: Gun

    apple: Gun
    aug: Gun
    awm: Gun
    beryl: Gun
    crossbow: Gun
    dp28: Gun
    groza: Gun
    hegrenade: Gun
    kar98k: Gun
    m16a4: Gun
    m24: Gun
    m249: Gun
    mini14: Gun
    mk14: Gun
    molotov: Gun
    mp5k: Gun
    mutant: Gun
    qbu: Gun
    qbz: Gun
    s12k: Gun
    s686: Gun
    s1897: Gun
    scarl: Gun
    skorpion: Gun
    sks: Gun
    slr: Gun
    tommy: Gun
    vss: Gun
