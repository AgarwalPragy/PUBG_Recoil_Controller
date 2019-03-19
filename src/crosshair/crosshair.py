from PIL import Image
import tkinter as tk
import sys
import win32gui
from win32api import GetSystemMetrics
import time

class Crosshair:

    def __init__(self, crosshair_color="(0, 255, 0, 255)", settings=(1, 3, 2, 1), fps=500):
        self.crosshair_color_rgba = eval(crosshair_color)
        self.crosshair_color_rgb = self.crosshair_color_rgba[:3]
        self.crosshair_color_int = int("%02x%02x%02x" % (self.crosshair_color_rgb[2], self.crosshair_color_rgb[1], self.crosshair_color_rgb[0]), 16)
        self.outline_color_int = 0
        self.filename = "crosshair.png"
        self.transparent_color = (255, 255, 255, 0)
        self.thickness = settings[0]
        self.length = settings[1]
        self.offset = settings[2]
        self.outline = settings[3]
        self.fps = fps
        self.allow_draw = True

        self.width = (self.length * 2) + self.thickness + (self.offset * 2)
        self.crosshair_matrix = []

    def create_crosshair_matrix(self):
        for y in range(self.width):
            row = []
            for x in range(self.width):
                append_flag = False

                # Create vertical lines
                if x >= (self.width / 2) - (self.thickness / 2) and x < self.length + self.offset + self.thickness:
                    if y < self.length:
                        row.append(self.crosshair_color_int)
                        append_flag = True
                    elif y >= self.length + (self.offset * 2) + self.thickness:
                        row.append(self.crosshair_color_int)
                        append_flag = True

                    if self.outline and append_flag and self.outline_color_int not in row:
                        row[len(row) - 2] = self.outline_color_int

                # Create horizontal lines
                if y >= (self.width / 2) - (self.thickness / 2) and y < self.length + self.offset + self.thickness:
                    if x < self.length:
                        row.append(self.crosshair_color_int)
                        append_flag = True
                    elif x >= self.length + (self.offset * 2) + self.thickness:
                        row.append(self.crosshair_color_int)
                        append_flag = True

                    if self.outline and append_flag and self.crosshair_color_int != self.crosshair_matrix[y - 1][x]:
                        self.crosshair_matrix[y - 1][x] = self.outline_color_int

                if not append_flag:
                    row.append(self.transparent_color)
            self.crosshair_matrix.append(row)

    def save_crosshair_png(self):
        im = Image.new("RGBA", (self.width, self.width))
        for y in range(self.width):
            for x in range(self.width):
                im.putpixel((x, y), self.crosshair_matrix[y][x])
        im.save(self.filename)

    def print_crosshair(self):
        for y in range(self.width):
            for x in range(self.width):
                if self.crosshair_matrix[y][x] == self.crosshair_color_int:
                    sys.stdout.write("1")
                elif self.crosshair_matrix[y][x] == self.outline_color_int:
                    sys.stdout.write("o")
                else:
                    sys.stdout.write("0")
            sys.stdout.write("\n")

    def draw_crosshair_pixels(self):
        coords = []
        sleep_time = t = 1 / self.fps
        w = GetSystemMetrics(0) / 2 - self.width / 2 #+ 1
        h = GetSystemMetrics(1) / 2 - self.width / 2 #+ 1
        dc = win32gui.GetDC(0)

        for y in range(self.width):
            for x in range(self.width):
                if self.crosshair_matrix[y][x] != self.transparent_color:
                    coords.append((int(x + w), int(y + h), self.crosshair_matrix[y][x]))

        while self.allow_draw:
            list(map(lambda x: win32gui.SetPixel(dc, x[0], x[1], x[2]), coords))
            time.sleep(sleep_time)

    def display_crosshair_window(self):

        def center(toplevel):
            toplevel.update_idletasks()
            w = toplevel.winfo_screenwidth()
            h = toplevel.winfo_screenheight()
            x = int(w / 2 - self.width / 2)
            y = int(h / 2 - self.width / 2)
            toplevel.geometry("{}x{}+{}+{}".format(self.width, self.width, x, y))

        root = tk.Tk()
        w = tk.Toplevel(root)
        w.title("Crosshair")
        w.geometry("250x80")
        button = tk.Button(w, text="Quit", command=root.destroy, height = 80, width = 250)
        button.pack()

        center(root)
        root.image = tk.PhotoImage(file=self.filename)
        label = tk.Label(root, image=root.image, bg='white')
        label.pack()
        root.overrideredirect(True)
        root.geometry("{}x{}".format(self.width, self.width))
        root.lift()
        root.wm_attributes("-topmost", True)
        root.wm_attributes("-disabled", True)
        root.wm_attributes("-transparentcolor", "white")
        label.mainloop()
