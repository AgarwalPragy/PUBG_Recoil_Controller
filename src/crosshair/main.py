from .crosshair import Crosshair
import json
import threading


def reload_crosshair(c = None):
    if c:
        c.allow_draw = False

    try:
        with open("config.json", "r") as f:
            config = json.loads(f.read())
        c = Crosshair(config["color"], (config["thickness"], config["length"], config["offset"], config["outline"]), config["set_pixel_fps"])
    except:
        print("Config error. Using default config.")
        c = Crosshair()

    c.create_crosshair_matrix()
    c_thread = threading.Thread(target=c.draw_crosshair_pixels)
    c_thread.daemon = True
    c_thread.start()
    return c


def update_config(key, value):
    config = {
        "color": "(0,255,0,255)",
        "length": 3,
        "offset": 2,
        "set_pixel_fps": 500,
        "thickness": 1,
        "outline": 1
    }
    try:
        with open("config.json", "r") as f:
            config = json.loads(f.read())
    except:
        with open("config.json", "w") as f:
            f.write("")

    if key == "color":
        config[key] = value
    else:
        config[key] = int(value)


    with open("config.json", "w") as f:
        f.write(json.dumps(config, indent=4, sort_keys=True))

def main():
    c = reload_crosshair()
    commands = ["thickness", "length", "offset", "color", "set_pixel_fps", "outline"]
    command = ""
    while command != "exit":
        command = input("crosshair> ")

        try:
            key, value = command.split(" ")
            if key in commands:
                update_config(key, value)
        except:
            if command not in ("exit", ""):
                print("Invalid command\n")
                print("Commands :")
                for command in commands:
                    print(command + " <value>")
                print("\n")

        c = reload_crosshair(c)


if __name__ == "__main__":
    main()
