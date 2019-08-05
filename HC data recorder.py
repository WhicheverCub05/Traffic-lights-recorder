from PIL import ImageGrab
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import ImageOps
import pytesseract
import cv2
import time
import numpy as np
import pyautogui
from scipy import misc

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
    image_np = np.array(image)
    cv2.imshow('', image_np)
    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyWindow('')


def image_grab(number):
    if number == 1:  # OEE
        capture = ImageGrab.grab(bbox=(900, 164, 1060, 188))

    elif number == 2:  # total speed losses
        capture = ImageGrab.grab(bbox=(420, 164, 500, 186))

    elif number == 3:  # actual performance losses
        capture = ImageGrab.grab(bbox=(172, 144, 253, 170))

    elif number == 4:  # actual runtime
        capture = ImageGrab.grab(bbox=(172, 112, 253, 138))

    elif number == 5:  # finished packs
        capture = ImageGrab.grab(bbox=(835, 640, 953, 665))

    elif number == 6:  # finished cases
        capture = ImageGrab.grab(bbox=(1440, 640, 1515, 665))

    else:
        capture = ImageGrab.grab(bbox=(0, 0, 1, 1))
        print("nothing was read")

    return capture


def process_image(image_to_process):
    image_sharpened = image_to_process.filter(ImageFilter.SHARPEN)
    image_sharpened_color = ImageEnhance.Color(image_sharpened).enhance(0)
    #  image_sharpened_color_contrast = ImageEnhance.Color(image_sharpened_color).enhance(1)
    image_sharpened_color_expand = ImageOps.expand(image_sharpened_color,  2, 0)
    # image_sharpened_color_expand_binary = image_sharpened_color_expand.convert('1')
    return image_sharpened_color_expand


def mouse_click(x, y):
    pyautogui.moveTo(x, y, duration=0.25)
    pyautogui.click()


def keyboard_type(key):
    pyautogui.typewrite(key, 0.25)


def increment_time():
    # OEE testbed
    mouse_click(900, 83)
    time.sleep(0.25)
    pyautogui.press('up')
    mouse_click(990, 73)
    time.sleep(2)
    # TO Finished packs
    mouse_click(822, 599)
    time.sleep(0.25)
    pyautogui.press('up')
    mouse_click(913, 587)
    time.sleep(2)
    # TO Finished cases
    mouse_click(1412, 598)
    time.sleep(0.25)
    pyautogui.press('up')
    mouse_click(1501, 586)
    time.sleep(2)


def ocr(image):
    time.sleep(0.25)
    value = pytesseract.image_to_string(image, config="--psm 13")
    time.sleep(1)
    print('value: ', value)
    if value == ' ':
        value = '0'
        return value
    else:
        return value


def correct_value(ocr_character):
    value = ocr_character
    value = value.translate({ord(i): None for i in ' '})
    value = value.translate({ord(i): None for i in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                                                   ',</?;|[{!@#$%^&*()]}'})
    return value


def correct_list(list_to_correct):
    corrected_list = []
    for i in range(0, len(list_to_correct)):
        list_value = list_to_correct[i]
        corrected_list_value = correct_value(list_value)
        corrected_list.append(corrected_list_value)
    return corrected_list


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


def correct_list(value_count, valueList, iterations):
    for i in range(0, iterations):  # len(valueList) // value_count
        number = i * value_count
        for j in range(0, len(valueList)):
            value = correct_value(valueList[j])
            print('number: ', number)
            number += 1
            number_figure.append(value)
            print(number_figure)# number_figure.append
        number_figureList.append(number_figure)
        print('number fig appended: ', number_figureList)# number_figure
        if len(number_figureList) < iterations:
            del number_figure[0:len(number_figure)]
        else:
            print(number_figureList)
            return number_figureList
'''


def split_list(list_of_values, iterations, value_count, current_iteration):
    temporary_list = []
    for j in range(0, value_count):
         index = current_iteration * iterations + j
         temporary_list.append(list_of_values[index])

    return temporary_list


def reconstruct_list(list_of_values, iterations, value_count):
    constructed_list = []
    current_iteration = 0
    for i in range(0, iterations):
        constructed_list.append(split_list(list_of_values, iterations, value_count, current_iteration))
        current_iteration += 1
    print(constructed_list)
    return constructed_list


'''
def correct_list(value_count, valueList):
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
'''


def write_to_excel(values, iterations, value_count):
    mouse_click(288, 855)
    time.sleep(1)
    for i in range(0, iterations):

        for j in range(0, value_count):  # len(number_figureList)
            pyautogui.press('down')
            keyboard_type('{}'.format(values[i][j]))

        pyautogui.press('right')
        for k in range(0, value_count):
            pyautogui.press('up')


'''
def write_to_excel(values, iterations, value_count):
    mouse_click(350, 695)
    hInc = 70
    vInc = 15
    for i in range(0, iterations):
        mouse_click(350+(i*hInc), 695)
        for j in range(0, value_count):  # len(number_figureList)
            mouse_click(350+(i*hInc), 695+((j % value_count)*vInc))
            keyboard_type('{}'.format(values[i][j]))


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


def main_sequence(iterations, value_count):
    for i in range(0, iterations):
        start_time = time.time()
        increment_time()
        for j in range(0, value_count):
            image = image_grab(j+1)
            processed_image = process_image(image)
            value = ocr(processed_image)
            ocr_figure.append(value)
        run_time = time.time() - start_time
        print('run_time: ', run_time)
        print('sleep time: ', 60-run_time)
        time.sleep(60-run_time)


def the_thing():
    iterations = int(3)
    value_count = int(6)
    main_sequence(iterations, value_count)
    corrected_list = correct_list(ocr_figure)
    constructed_list = reconstruct_list(corrected_list, iterations, value_count)
    write_to_excel(constructed_list, iterations, value_count)


def test_ocr():
    image = image_grab(int(input('enter the grab: ')))
    ocr(image)
    processed_image = process_image(image)
    display_image(processed_image)


def test_mouse():
    found = False
    while not found:
        print(pyautogui.position())
        time.sleep(1)
        if cv2.waitKey(20) == 27:
            print("found position: ", pyautogui.position())
            found = True
            break


run = False


while not run:
    answer = input('do the thing? y/n/test: ')
    try:
        answer = str(answer)
    except:
        print('input a letter')
    if answer == 'y' or answer == 'Y':
        print('Terminate the program by pressing CTRL+C')
        time.sleep(5)
        the_thing()
        run = True
    elif answer == 'n' or answer == 'N':
        print('closing program')
        time.sleep(2)
        break
    elif answer.lower() == 'test':
        test_run = True
        while test_run:
            try:
                test_type = input('capture zone or mouse move or quit(c/m/q)?').lower()
            except ValueError:
                print('only input c or m or q')
                test_type = ' '

            if test_type == 'c':
                while True:
                    test_ocr()

            elif test_type == 'm':
                while True:
                    test_mouse()

            elif test_type == 'q':
                test_run = False

            else:
                print('input a valid character')
    else:
        print('input a valid character')


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
'''
