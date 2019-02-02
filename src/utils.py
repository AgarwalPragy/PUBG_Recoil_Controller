from ctypes import windll, c_uint
import config
import win32gui


def is_game_in_foreground() -> bool:
    return config.game_window_text == win32gui.GetWindowText(win32gui.GetForegroundWindow())


def in_game_mouse_move(y_relative: int):
    windll.user32.mouse_event(
        c_uint(0x0001),
        c_uint(0),
        c_uint(y_relative),
        c_uint(0),
        c_uint(0)
    )

