from PIL import ImageGrab
import pytesseract
import cv2
import time
import numpy as np
import pyautogui

#  Available Libraries = os, argparse, Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\Tesseract.exe'

tempList = []

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
        capture = ImageGrab.grab(bbox=(950, 186, 1091, 206))
        capture_np = np.array(capture)

    elif number == 2:
        capture = ImageGrab.grab(bbox=(440, 184, 500, 206))
        capture_np = np.array(capture)

    elif number == 3:
        capture = ImageGrab.grab(bbox=(173, 162, 234, 190))
        capture_np = np.array(capture)

    elif number == 4:  # actual runtime
        capture = ImageGrab.grab(bbox=(170, 122, 234, 153))
        capture_np = np.array(capture)

    elif number == 5:  # finished packs
        capture = ImageGrab.grab(bbox=(825, 640, 953, 665))
        capture_np = np.array(capture)

    elif number == 6:  # finished cases
        capture = ImageGrab.grab(bbox=(1429, 633, 1505, 670))
        capture_np = np.array(capture)

    else:
        capture = ImageGrab.grab(bbox=(0, 0, 1, 1))
        capture_np = np.array(capture)
        print("nothing was read")

    return capture_np


def mouse_click(x, y):
    pyautogui.moveTo(x, y, duration=0.25)
    pyautogui.click()


def keyboard_type(key):
    pyautogui.typewrite(key, 0.25)


def increment_time(starting_min):
    # OEE testbed
    mouse_click(700, 77)
    time.sleep(0.25)
    keyboard_type('0{}'.format(starting_min))
    mouse_click(800, 70)
    time.sleep(2)
    # TO Finished packs
    mouse_click(637, 495)
    time.sleep(0.25)
    keyboard_type('0{}'.format(starting_min))
    mouse_click(720, 485)
    time.sleep(2)
    # TO Finished cases
    mouse_click(1120, 495)
    time.sleep(0.25)
    keyboard_type('0{}'.format(starting_min))
    mouse_click(1205, 485)
    time.sleep(2)


def ocr(image):
    time.sleep(0.25)
    value = pytesseract.image_to_string(image)
    time.sleep(0.25)
    print('value: ', value)
    if value == ' ':
        value = '0'
        return value
    else:
        return value


def correct_value(ocr_character):
    value = ocr_character
    value.replace(' ', '')  # removes spaces
    value = value.translate({ord(i): None for i in ' '})
    value = value.translate({ord(i): None for i in 'abcdefghijklmnopqrstuvwxyz,</?;|[{!@#$%^&*()]}'})
    return value


def make_excel_list(values, iterations, value_count):
    for i in range(0, ((len(values)) // value_count)):
        listCounter = i * value_count
        for j in range(0, value_count):
            tempList.append(values[listCounter])
            listCounter += 1
        ocr_figureList.append(tempList)
        print('ocr: ', ocr_figureList)
        if len(ocr_figureList) == iterations:
            return ocr_figureList
        else:
            pass
        del tempList[0:value_count]



def correct_list(value_count, valueList, valueListList):
    for i in range(0, len(valueList)//value_count):
        number = i * value_count
        for j in range(0, len(valueList)):
            value = correct_value(valueList[j])
            print('number: ', number)
            number += 1
            number_figure.append(value)  # number_figure.append
        number_figureList.append(number_figure)  # number_figure
    print("corrected list: ", number_figureList)
    return_list = number_figureList
    return return_list


def write_to_excel(values, iterations, value_count):
    mouse_click(350, 695)
    hInc = 70
    vInc = 15
    for i in range(0, iterations):
        mouse_click(350+(i*hInc), 695)
        for j in range(0, value_count):  # len(number_figureList)
            mouse_click(350+(i*hInc), 695+((j % value_count)*vInc))
            keyboard_type('{}'.format(values[i][j]))
'''

def make_excel_list(values, iterations, value_count):
    for i in range(0, ((len(values)) // value_count)):
        listCounter = i * value_count
        for j in range(0, value_count):
            tempList.append(values[listCounter])
            listCounter += 1
        ocr_figureList.append(tempList)
        print('ocr: ', ocr_figureList)
        if len(ocr_figureList) == iterations:
            return ocr_figureList
        else:
            pass
        del tempList[0:value_count]
'''

def main_sequence(iterations, interval_time, value_count):
    for i in range(0, iterations):
        increment_time(i)
        time.sleep(interval_time)
        for j in range(0, value_count):
            image = image_grab(j+1)
            value = ocr(image)
            #display_image(image)
            ocr_figure.append(value)


def the_thing():
    interval_time = 2
    iterations = int(10)
    value_count = int(6)
    main_sequence(iterations, interval_time, value_count)
    compiledList = make_excel_list(ocr_figure, iterations, value_count)
    corrected_list = correct_list(value_count, ocr_figure, compiledList)
    write_to_excel(corrected_list, iterations, value_count)


while True:
    answer = input('do the thing? y/n: ')
    try:
        answer = str(answer)
    except:
        print('input a letter')
    if answer == 'y':
        print('Terminate the program by pressing CTRL+C')
        time.sleep(5)
        the_thing()
    elif answer == 'n':
        print('closing program')
        time.sleep(2)
        break
    elif answer.lower() == 'test':
        while True:
            image = image_grab(int(input('enter the grab: ')))
            ocr(image)
            display_image(image)

    else:
        print('enter the correct input')


'''
main_sequence(iterations, interval_time)
usableList = make_excel_list(ocr_figure, iterations, value_count)
print(usableList)
write_to_excel(usableList, iterations, value_count)
'''
# ssssssssssssssssssssssssssssssssssssssssssssssssssssss

'''
def test_sequence():
    time_increment = 0
    for j in range(0, 3):
        image_to_process = image_grab(j+1)
        ocr_value = (ocr(image_to_process))
        display_image(image_to_process)
        ocr_figure.append(ocr_value)
    ocr_figureList.append(ocr_figure)
    time_increment += 1
    time.sleep(2)
    increment_time(time_increment % 60)
    print("ocr_figureList: ", ocr_figureList)


for i in range(0, 2):
    test_sequence()
correct_list()
write_to_excel()



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
