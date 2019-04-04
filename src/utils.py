from ctypes import windll, c_uint
import config
import win32gui


def is_game_in_foreground() -> bool:
    return config.game_window_text == win32gui.GetWindowText(win32gui.GetForegroundWindow())


index = 0


def in_game_mouse_move(y_relative: int):
    global index
    index = (index + 1) % 9
    windll.user32.mouse_event(
        c_uint(0x0001),
        c_uint(int(index%2 == 1)),  # 4 / 9 times
        c_uint(y_relative),
        c_uint(0),
        c_uint(0)
    )

