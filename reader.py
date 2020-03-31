# This file reads data from the tags
import csv
import threading
import tkinter as tk

import RPi.GPIO as GPIO
from PIL import ImageTk, Image
from mfrc522 import SimpleMFRC522


class GuiInfo:

    def __init__(self, window: tk.Tk):
        self.window = window
        self.properties = {}

    def change_image(self, path: str):
        if 'panel' in self.properties.keys():
            i = ImageTk.PhotoImage(Image.open(path))
            self.properties['panel'].configure(image=i)
            self.properties['panel'].image = i
            self.window.update()
        else:
            raise AttributeError('Panel not yet configured.')


def main():
    window = tk.Tk()
    window.title("ZipCard")
    window.geometry("500x600")
    window.configure(background='grey')
    info = GuiInfo(window)
    panel = tk.Label(window)
    info.properties['panel'] = panel
    panel.pack(side="bottom", fill="both", expand="yes")

    reader = threading.Thread(target=do_read, args=(info,))
    reader.start()

    window.mainloop()


def do_read(info: GuiInfo):
    rd = SimpleMFRC522()

    try:
        print("Tap tag to reader")
        id, text = rd.read()
        print(text)
        text = text.strip()
        process_csv(text, info)

    finally:
        GPIO.cleanup()


def process_csv(file, info: GuiInfo):
    with open(file, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\tProduct: {row[0]}, Price: {row[1]}, Nutrition facts: {row[2]}')
                image_path = row[2]
                try:
                    info.change_image(row[2])
                except IOError:
                    print("Unable to retrieve nutrition facts")
                line_count += 1


if __name__ == '__main__':
    main()
