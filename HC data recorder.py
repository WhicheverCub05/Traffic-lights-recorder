from PIL import ImageGrab
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import ImageOps
import pytesseract
import cv2
import time
import numpy as np
import pyautogui

#  Available Libraries = os, argparse, Image, scipy

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\Tesseract.exe'

tempList = []

ocr_figure = []
ocr_figureList = []

number_figure = []
number_figureList = []


oee_pie_key_value_pair = {
    1: 'Producing Time',
    2: 'Speed Losses',
    3: 'Speed Losses - Can',
    4: 'Machine Short Stops',
    5: 'Machine Long Stops',
    6: 'Utilities Outage',
    7: 'Materials Short Stops',
    8: 'Materials Long Stops',
    9: 'Meetings',
    10: 'Changeover',
    11: 'Asset Care (Scheduled Time)'
}


def open_image(picture_name):
    image = cv2.imread(picture_name)
    return image


def display_image(image):
    image_np = np.array(image)
    cv2.imshow('', image_np)
    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyWindow('')


def image_grab_oee_pie_times(number, iteration_number):
    iteration_number = iteration_number
    key_list = [['pgt', 0],
                ['sdl', -9],
                ['sdlc', 18],
                ['mess', 28],
                ['mels', 24],
                ['uso', 2],
                ['mlss', 26],
                ['mlls', 23],
                ['ms', -28],
                ['cr', -11],
                ['atc', 66]]
    print('number: ', number)
    print('key_list_number', key_list[number][1])
    base_left = 110 + key_list[number][1]
    base_top = 92 + (20 * iteration_number)
    base_right = 190
    base_bottom = base_top + 20
    capture = ImageGrab.grab(bbox=(base_left, base_top, base_right, base_bottom))

    print('returning capture in image_grab_pie')

    return capture


def image_grab_oee_pie_percentage(number):
    if number == 12:  # Total Time
        capture = ImageGrab.grab(bbox=(62, 400, 190, 420))

    elif number == 13:  # OEE
        capture = ImageGrab.grab(bbox=(31, 425, 190, 445))

    elif number == 14:  # Availability rate
        capture = ImageGrab.grab(bbox=(90, 445, 190, 465))

    elif number == 15:  # Performance rate
        capture = ImageGrab.grab(bbox=(98, 460, 190, 485))

    elif number == 16:  # Quality rate
        capture = ImageGrab.grab(bbox=(71, 480, 190, 505))

    else:
        capture = ImageGrab.grab(bbox=(0, 0, 1, 1))

    return capture


def image_grab_oee_testbed(number):
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
        cv2.destroyAllWindows()

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


def increment_time_oee_pie(number_of_min_interval):
    mouse_click(830, 75)
    time.sleep(1)
    for i in range(0, number_of_min_interval):
        pyautogui.press('up')
    mouse_click(910, 60)
    time.sleep(2)


def increment_time_oee_testbed():
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
    if value == ' ':
        value = '0'
        return value
    else:
        return value


def correct_value(ocr_character):
    value = ocr_character
    value = value.translate({ord(i): None for i in ' '})
    value = value.translate({ord(i): None for i in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                                                   ',</?;|[{!@#$%^&*()]}=-_+'})
    return value


def correct_list(list_to_correct):
    corrected_list = []
    print('list to correct in correct_list: ', list_to_correct)
    for i in range(0, len(list_to_correct)):
        list_value = list_to_correct[i]
        corrected_list_value = correct_value(list_value)
        corrected_list.append(corrected_list_value)
        print('correcting list: ', corrected_list)
    return corrected_list


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


def write_to_excel(values, iterations, value_count, setup):
    #clicks on the cell just above the data input
    if setup == 'op':
        mouse_click(240, 700)
        mouse_click(240, 700)
    else:
        mouse_click(320, 755)
        mouse_click(320, 755)
    time.sleep(1)
    for i in range(0, iterations):

        for j in range(0, value_count):  # len(number_figureList)
            pyautogui.press('down')
            keyboard_type('{}'.format(values[i][j]))

        pyautogui.press('right')
        for k in range(0, value_count):
            pyautogui.press('up')


def oee_testbed_run_sequence(iterations, value_count, interval_min):
    for i in range(0, iterations):
        start_time = time.time()
        #increment_time_oee_testbed()
        mouse_click(916, 50)
        for j in range(0, value_count):
            image = image_grab_oee_testbed(j+1)
            processed_image = process_image(image)
            value = ocr(processed_image)
            ocr_figure.append(value)
        run_time = time.time() - start_time
        print('run_time: ', run_time)
        print('sleep time: ', (interval_min*60)-run_time)
        time.sleep((interval_min*60)-run_time)


def assign_oee_pie_capture_zone_test(grab):
    if grab < 12:
        iteration = int(input('iteration number?: '))
        image = image_grab_oee_pie_times(iteration-1, grab-1)
    else:
        image = image_grab_oee_pie_percentage(grab)

    return image


def assign_oee_pie_capture_zone(grab, iteration):
    print('assign numbers (grab): ', grab, '(iteration): ', iteration)
    if grab < 12:
        image = image_grab_oee_pie_times(grab, iteration-1)
    else:
        image = image_grab_oee_pie_percentage(grab)

    return image


def oee_pie_run_sequence(iterations, value_count, interval_min, value_list):
    bottom_values = [12, 13, 14, 15, 16]
    map_list(1, value_list)
    print('got to the pie_run_sequence')

    for i in range(0, len(bottom_values)):
        value_list.append(bottom_values[i])

    print('value_count: ', value_count)

    for i in range(0, iterations):
        start_time = time.time()
        increment_time_oee_pie(interval_min)
        print('val_list in oee_pie_seq: ', value_list)

        for j in range(0, value_count):
            image = assign_oee_pie_capture_zone(value_list[j], j)
            processed_image = process_image(image)
            value = ocr(processed_image)
            ocr_figure.append(value)

        run_time = time.time() - start_time
        print('run_time: ', run_time)
        print('sleep time: ', (interval_min*60)-run_time)
        #time.sleep((interval_min*60)-run_time)


def the_thing(which_thing, interval_min, value_list):
    if which_thing == 'ot':
        iterations = int(input('how many columns of data would you like to collect?: '))
        value_count = int(input('how many values?: '))
        oee_testbed_run_sequence(iterations, value_count, interval_min)
    else:
        iterations = int(input('how many columns of data would you like to collect?: '))
        value_count = len(value_list)
        oee_pie_run_sequence(iterations, value_count, interval_min, value_list)
    corrected_list = correct_list(ocr_figure)
    constructed_list = reconstruct_list(corrected_list, iterations, value_count)
    write_to_excel(constructed_list, iterations, value_count, which_thing)


def test_ocr(setup, grab):
    if setup == 'op':
        image = assign_oee_pie_capture_zone_test(grab)
    elif setup == 'ot':
        image = image_grab_oee_testbed(grab)
    else:
        image = image_grab_oee_testbed(7)

    processed_image = process_image(image)
    print('ocr value read: ', correct_value(ocr(processed_image)))
    display_image(processed_image)


def test_mouse():
    found = False
    while not found:
        print(pyautogui.position())
        time.sleep(2)
        k = cv2.waitKey(0)
        if k == 15:
            print("found position: ", pyautogui.position())

        if k == 27:
            print('ending')
            time.sleep(2)
            break


def map_list(map_by, list_to_map):
    for i in range(0, len(list_to_map)):
        list_to_map[i] = (list_to_map[i]-map_by)


def make_str_list_into_int_list(str_list):
    for i in range(0, len(str_list)):
        str_list[i] = int(str_list[i])
    return str_list


run = False

while not run:
    answer = input('do the thing? y/n/test: ')
    try:
        answer = str(answer)
    except:
        print('input a letter')
    if answer == 'y' or answer == 'Y':
        which_thing = input('OEE testbed or OEE pie? (OP/OT): ').lower()
        if which_thing == 'op':
            user_time_interval = int(input('how many minutes between intervals?: '))
            for k, v in oee_pie_key_value_pair.items():
                print(k, v)
            value_list = input('input a comma-separated list of the corresponding number you want: ').split(', ')
            int_value_list = make_str_list_into_int_list(value_list)
            print(value_list)
            time.sleep(2)
            the_thing(which_thing, user_time_interval, value_list)

        elif which_thing == 'ot':
            user_time_interval = int(input('how many minutes between intervals?: '))
            value_list = []
            time.sleep(2)
            the_thing(which_thing, user_time_interval, value_list)

    elif answer == 'n' or answer == 'N':
        print('closing program')
        time.sleep(2)
        break

    elif answer.lower() == 'test':
        test_selection = True
        while test_selection:

            test_run = True
            while test_run:
                try:
                    test_type = input('capture zone or mouse move or quit(c/m/q)?').lower()
                except ValueError:
                    print('only input c or m or q')
                    test_type = ' '

                if test_type == 'c':
                    while True:
                        setup = input('which setup? OEE testbed or OEE pie? (ot/op)/(q to quit)').lower()
                        grab = int(input('which zone?: '))
                        if setup == 'q':
                            test_selection = False
                            break
                        else:
                            test_ocr(grab=grab, setup=setup)

                elif test_type == 'm':
                    while True:
                        test_mouse()

                elif test_type == 'q':
                    test_run = False

                else:
                    print('input a valid character')
    else:
        print('input a valid character')

    run = True


'''
def oee_pie_run_sequence(iterations, value_count, interval_min, value_list):
    bottom_values = [12, 13, 14, 15, 16]
    map_list(1, value_list)
    print('got to the pie')

    for i in range(0, len(bottom_values)):
        value_list.append(bottom_values[i])

    for i in range(0, iterations):
        start_time = time.time()
        increment_time_oee_pie(interval_min)
        print('val_list in oee_pie_seq: ', value_list)

        for j in range(0, value_count):
            print('j: ', j)
            print('value_list[j-1]: ', value_list[j - 1])
            image = image_grab_oee_pie_times(value_list[j - 1], j)
            processed_image = process_image(image)
            time.sleep(1)
            value = ocr(processed_image)
            ocr_figure.append(value)

        for j in range(0, value_count):
            print('k', j)
            image = image_grab_oee_pie_percentage(value_list[j + 11])
            processed_image = process_image(image)
            value = ocr(processed_image)
            ocr_figure.append(value)

        run_time = time.time() - start_time
        print('run_time: ', run_time)
        print('sleep time: ', (interval_min * 60) - run_time)
        time.sleep((interval_min * 60) - run_time)
'''
