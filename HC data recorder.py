from PIL import Image
from PIL import ImageGrab
import pytesseract
import argparse
import cv2
import os
import time
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\Tesseract.exe'


ocr_figure = []
ocr_figureList = []

number_figure = []
number_figureList = []


def open_image(pictureName):
    image = cv2.imread(pictureName)
    return image


def display_image(image):
    cv2.imshow('', image)
    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyWindow('')


def image_grab(number):
    if number == 1:
        capture = ImageGrab.grab(bbox=(970, 186, 1017, 206))
        capture_np = np.array(capture)

    if number == 2:
        capture = ImageGrab.grab(bbox=(445, 186, 510, 206))
        capture_np = np.array(capture)

    if number == 3:
        capture = ImageGrab.grab(bbox=(172, 166, 242, 186))
        capture_np = np.array(capture)

    return capture_np


def ocr(image):
    return pytesseract.image_to_string(image)



def correct_value(ocr_character):
    value = ocr_character
    value.replace(' ', '')  # removes spaces
    value.replace('abcdefghijklmnopqrstuvwxyz,</?;'"|[{]}", '')
    return value


def correct_list(value):
    for i in range(0, len(ocr_figureList)-1):
        for i in range(0, len(ocr_figure)-1):
            pass
        pass


def test_sequence():
    for i in range(0, 2):
        image_to_process = image_grab(i+1)
        print(ocr(image_to_process))
        display_image(image_to_process)

        ocr_figure.append(ocr_figure)
    ocr_figureList.append(ocr_figure)



'''
while not keybreak:
    k = cv2.waitKey(0)
    image1 = open_image("image.png")
    display_image(image1)
    time.sleep(3)
    cv2.destroyWindow('')
    print(pytesseract.image_to_string(image1))
    if k == 27:
        keybreak = True
        break


def ocr():
  

def screen_capture():


def write_data():


def mouse_move():


def mouse_click():


def input_data():


def increment_time():


def picture_naming():
    return picture_name
    

'''