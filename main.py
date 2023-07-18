import Speech_to_Text as sp
import Browser as br
from selenium.webdriver.common.by import By
import time
import pyautogui

audio_query = sp.obtain_audio_from_mic("Please say the term you want to search")
text_query = sp.convert_speech_to_text(audio_query)
br_obj = br.Browser()
br_obj.perform_google_search(text_query)
br_obj.accept_google_cookies()


def move_mouse(direction, num):
    current_x, current_y = pyautogui.position()
    if num != None:
        if '.' in num:
            num = num.replace('.', '')
        if num.lower() == 'χείλια' or num.lower() == 'κοιλιά':
            num = '1000'
        num = int(num)
    else:
        num = 10

    if direction == 'κάτω':
        new_x = current_x
        new_y = current_y + num
        if new_y > pyautogui.size().height:
            # Scroll the page down if mouse goes out of sight
            pyautogui.press('down', presses=9)
    elif direction == 'πάνω' or direction == 'πάνο':
        new_x = current_x
        new_y = current_y - num
        if new_y < 0:
            # Scroll the page up if mouse goes out of sight
            pyautogui.press('up', presses=9)
    elif direction == 'δεξιά':
        new_x = current_x + num
        new_y = current_y
    elif direction == 'αριστερά':
        new_x = current_x - num
        new_y = current_y
    else:
        return  # Invalid direction

    pyautogui.moveTo(new_x, new_y, duration=0.5)


while True:
    audio_query = sp.obtain_audio_from_mic(None)
    time.sleep(2)
    text_query = sp.convert_speech_to_text(audio_query)
    print(text_query)

    query_parts = text_query.split()
    if len(query_parts) != 2:
        if text_query.lower() == 'κλικ':
            pyautogui.click()  # Perform a mouse click
        elif text_query.lower() == 'πίσω':
            br_obj.driver.back()  # Go back to the previous page
        continue  # Go back to the beginning of the loop if number of query parts is not 2
    else:
        direction, num = query_parts
        try:
            num = int(num)
        except:
            continue

    direction, num = query_parts
    move_mouse(direction.lower(), num.lower())
