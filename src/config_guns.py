from Enums import *
from Entitites import *

__all__ = []


# =============================================================================================
#  AR

Guns.m416 = Gun(
    name='m416',
    type_=GunTypes.full_auto,
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
    horizontal_recoil=[0] * 40,
)

Guns.akm = Gun(
    name='akm',
    type_=GunTypes.full_auto,
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
    horizontal_recoil=[0] * 6 + [1, 0] * 17,
)

Guns.g36c = Gun(
    name='g36c',
    type_=GunTypes.full_auto,
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
    horizontal_recoil=[0] * 40,
)

Guns.dp28 = Gun(
    name='dp28',
    type_=GunTypes.full_auto,
    time_between_shots=0.118,
    vertical_recoil=[
        11, 24, 24, 24, 30,
        35, 37, 40, 42, 45,
        47, 47, 52, 52, 52,
        52, 52, 52, 52, 52,
        52, 52, 53, 53, 53,
        54, 54, 54, 54, 54,
        55, 55, 55, 55, 55,
        56, 56, 56, 56, 56,
        57, 57, 57, 57, 57,
        58, 58,
    ],
    horizontal_recoil=[0] * 47,
)

Guns.beryl = Gun(
    name='beryl',
    type_=GunTypes.full_auto,
    time_between_shots=0.1,
    vertical_recoil=[
        20, 26, 26, 26, 30,
        42, 42, 42, 45, 47,
        49, 50, 50, 55, 55,
        60, 60, 60, 60, 60,
        62, 62, 62, 63, 64,
        62, 62, 62, 63, 64,
        64, 64, 64, 64, 64,
        64, 64, 64, 64, 64,
    ],
    horizontal_recoil=[0] * 40,
)


Guns.m16a4 = Gun(
    name='m16a4',
    type_=GunTypes.single_fire,
    time_between_shots=1/7,
    vertical_recoil=[
        13, 17, 18, 26, 27,
        27, 28, 29, 30, 30,
        30, 30, 31, 31, 32,
        32, 32, 33, 33, 34,
        33, 34, 33, 34, 33,
        34, 33, 34, 33, 34,
        33, 34, 33, 34, 33,
        34, 33, 34, 33, 34,
    ],
    horizontal_recoil=[0] * 40,
)

Guns.mutant = Gun.copy_from(Guns.m16a4, 'mutant')
Guns.aug = Gun.copy_from(Guns.m416, 'aug')
Guns.groza = Gun.copy_from(Guns.akm, 'groza')
Guns.m249 = Gun.copy_from(Guns.akm, 'm249')
Guns.mk14 = Gun.copy_from(Guns.akm, 'mk14')
Guns.qbz = Gun.copy_from(Guns.m416, 'qbz')
Guns.scarl = Gun.copy_from(Guns.m416, 'scarl')


# =============================================================================================
#  SMG

Guns.uzi = Gun(
    name='uzi',
    type_=GunTypes.full_auto,
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
    horizontal_recoil=[0] * 35,
)

Guns.bizon = Gun(
    name='bizon',
    type_=GunTypes.full_auto,
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
    horizontal_recoil=[0] * 11 + [1, 0] * 21,
)

Guns.vector = Gun(
    name='vector',
    type_=GunTypes.full_auto,
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
    horizontal_recoil=[0] * 11 + [1, 0] * 11,
)

Guns.ump45 = Gun(
    name='ump45',
    type_=GunTypes.full_auto,
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
    horizontal_recoil=[0] * 35,
)

Guns.mp5k = Gun.copy_from(Guns.ump45, 'mp5k')
Guns.tommy = Gun.copy_from(Guns.ump45, 'tommy')


# =============================================================================================
#  DMR


Guns.mini14 = Gun.copy_from(Guns.m16a4, 'mini14')
Guns.qbu = Gun.copy_from(Guns.m16a4, 'qbu')
Guns.sks = Gun.copy_from(Guns.m16a4, 'sks')
Guns.slr = Gun(
    name='slr',
    type_=GunTypes.single_fire,
    time_between_shots=1/4,
    vertical_recoil=[
        17, 19, 25, 27, 29,
    ],
    horizontal_recoil=[0] * 5,
)


# =============================================================================================
#  SR


Guns.sniper = Gun(
    name='sniper',
    type_=GunTypes.bolt_action,
    time_between_shots=1,
    vertical_recoil=[0]*100,
    horizontal_recoil=[0]*100,
)


Guns.vss = Gun.copy_from(Guns.bizon, 'vss')
Guns.awm = Gun.copy_from(Guns.sniper, 'awm')
Guns.kar98k = Gun.copy_from(Guns.sniper, 'kar98k')
Guns.m24 = Gun.copy_from(Guns.sniper, 'm24')


# =============================================================================================
#  Other


Guns.apple = Gun.copy_from(Guns.sniper, 'apple')
Guns.hegrenade = Gun.copy_from(Guns.sniper, 'hegrenade')
Guns.molotov = Gun.copy_from(Guns.sniper, 'molotov')
Guns.skorpion = Gun.copy_from(Guns.sniper, 'skorpion')

Guns.crossbow = Gun.copy_from(Guns.sniper, 'crossbow')

Guns.s12k = Gun.copy_from(Guns.sniper, 's12k')
Guns.s686 = Gun.copy_from(Guns.sniper, 's686')
Guns.s1897 = Gun.copy_from(Guns.sniper, 's1897')
