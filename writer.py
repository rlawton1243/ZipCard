# This file will be used to write to the RFID tags
# Data written is a file path to the product related to the tag
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


def main():
    reader = SimpleMFRC522()

    try:
        file = input('New data: ')
        print("Now place your tag to write")
        reader.write(file)
        print("Written")

    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
