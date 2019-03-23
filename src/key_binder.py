import time
import keyboard


def binder(key_code: int):
    def inner(event):
        time.sleep(1)
        keyboard.press_and_release(key_code)
        keyboard.unhook_all()
    return inner


if __name__ == '__main__':
    keyboard.on_press_key(59, binder(118))
    while True:
        time.sleep(0.05)
