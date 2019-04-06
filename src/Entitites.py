import itertools
import typing as T
from dataclasses import dataclass
from math import floor

__all__ = ['Screen', 'WeaponSlot', 'Zoom', 'Gun']


@dataclass(unsafe_hash=True)
class Screen:
    name: str
    is_default: bool
    symbol: str


@dataclass(unsafe_hash=True)
class WeaponSlot:
    name: str
    is_default: bool
    symbol: str


@dataclass(unsafe_hash=True)
class Zoom:
    name: str
    is_default: bool
    recoil_multiplier: float = 1.0


class Gun:
    name: str
    time_between_shots: float
    _vertical_recoil: T.List[int]
    _horizontal_recoil: T.List[int]
    _cumulative_vertical: T.List[int]
    _cumulative_horizontal: T.List[int]

    def __init__(self, name: str, time_between_shots: float, vertical_recoil: T.List[int], horizontal_recoil: T.List[int]) -> None:
        self.name = name
        self.time_between_shots = time_between_shots
        self._vertical_recoil = vertical_recoil
        self._horizontal_recoil = horizontal_recoil
        self._rebuild_recoil_tables()

    @property
    def recoil_per_second(self):
        recoil_per_bullet = sum(self.vertical_recoil) / len(self.vertical_recoil)
        seconds_per_bullet = self.time_between_shots
        return recoil_per_bullet / seconds_per_bullet

    @property
    def vertical_recoil(self):
        return self._vertical_recoil

    @vertical_recoil.setter
    def vertical_recoil(self, value: T.List[int]):
        self._vertical_recoil = value
        self._rebuild_recoil_tables()

    @property
    def horizontal_recoil(self):
        return self._horizontal_recoil

    @horizontal_recoil.setter
    def horizontal_recoil(self, value: T.List[int]):
        self._horizontal_recoil = value
        self._rebuild_recoil_tables()

    def _rebuild_recoil_tables(self) -> None:
        self._cumulative_vertical = list(itertools.accumulate(self.vertical_recoil))
        self._cumulative_horizontal = list(itertools.accumulate(self.horizontal_recoil))

    def get_mouse_move_amount(self, time_since_fire_start: float, x_moved: int, y_moved: int, multiplier: float) -> T.Tuple[int, int]:
        bullets_fired = self.get_bullets_fired(time_since_fire_start)
        if bullets_fired == len(self.vertical_recoil):
            return 0, 0
        time_since_last_bullet = time_since_fire_start - (bullets_fired - 1) * self.time_between_shots
        x_expected = self._cumulative_horizontal[bullets_fired-1] + self.horizontal_recoil[bullets_fired] * time_since_last_bullet / self.time_between_shots
        y_expected = self._cumulative_vertical[bullets_fired-1] + self.vertical_recoil[bullets_fired] * time_since_last_bullet / self.time_between_shots
        dx = multiplier * x_expected - x_moved
        dy = multiplier * y_expected - y_moved
        return int(dx), int(dy)

    def get_bullets_fired(self, time_since_fire_start: float) -> int:
        bullets_fired = floor(time_since_fire_start / self.time_between_shots) + 1   # add one because the first bullet gets fired when fire is pressed
        return min(len(self.vertical_recoil), bullets_fired)
