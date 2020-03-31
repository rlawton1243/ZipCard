# This file reads data from the tags
import csv

import RPi.GPIO as GPIO
from PIL import Image
from mfrc522 import SimpleMFRC522


def main():
    reader = SimpleMFRC522()

    try:
        print("Tap tag to reader")
        id, text = reader.read()
        print(text)
        text = text.strip()
        process_csv(text)

    finally:
        GPIO.cleanup()


def process_csv(file):
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
                    img = Image.open(row[2])
                    img.show()
                except IOError:
                    print("Unable to retrieve nutrition facts")
                line_count += 1


if __name__ == '__main__':
    main()
