import Speech_to_Text as sp
import Browser as br
import time
import pyautogui

class MouseController:
    def __init__(self):
        self.br_obj = br.Browser()
        self.num_of_search = 0
        self.search_bar_text = ""
        self.text_query = ""

        # Αρχικά το mouse cursor ξεκινάει από το κέντρο της οθόνης
        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(screen_width // 2, screen_height // 2)

    def type_in_search_bar(self):
        while True:
            # audio_query = sp.obtain_audio_from_mic(None)
            # self.text_query = sp.convert_speech_to_text(audio_query)
            # print(self.text_query)

            if self.text_query.lower() == "type":
                # Wait for user to speak after saying "type"
                audio_search = sp.obtain_audio_from_mic("Please say your search term")
                search_term = sp.convert_speech_to_text(audio_search)
                print(f'search term: {search_term}')

                if search_term != 0:
                    if search_term.lower() == "delete" or 'lidl' in search_term.lower():
                        # Delete the previous text in the search bar
                        pyautogui.click(clicks=4)
                        pyautogui.press("backspace")
                        self.search_bar_text = ""
                    else:
                        # Type the search term in the search bar
                        pyautogui.typewrite(self.search_bar_text + search_term)
                        self.search_bar_text = self.search_bar_text + search_term
                        pyautogui.press("enter")
                        break
            elif self.text_query.lower() == "delete" or self.text_query.lower() == "elite" or self.text_query.lower() == "διαγραφή":
                # Delete the previous text in the search bar
                pyautogui.press("backspace", presses=len(self.search_bar_text))
                self.search_bar_text = ""

    def start(self):
        while True:
            audio_query = sp.obtain_audio_from_mic("Please say the term you want to search")
            self.text_query = sp.convert_speech_to_text(audio_query)
            if self.text_query == 0:
                continue
            else:
                break

        self.br_obj.perform_google_search(self.text_query)
        if self.num_of_search == 0:
            self.br_obj.accept_google_cookies()

        while True:
            audio_query = sp.obtain_audio_from_mic(None)
            time.sleep(2)
            self.text_query = sp.convert_speech_to_text(audio_query)
            print(self.text_query)
            
            try:
                query_parts = self.text_query.split()
            except:
                continue

            if len(query_parts) != 2:
                if self.text_query.lower() == 'κλικ':
                    pyautogui.click()  # Perform a mouse click
                elif self.text_query.lower() == 'πίσω':
                    self.br_obj.driver.back()  # Go back to the previous page
                elif self.text_query.lower() == 'type':
                    self.type_in_search_bar()
                continue  # Go back to the beginning of the loop if the number of query parts is not 2

            if self.text_query.lower() == 'νέα αναζήτηση':
                self.num_of_search = 1
                self.search_bar_text = ""
                self.start()  # Start a new search

            direction, num = query_parts
            try:
                if num == 'χείλια' or num == 'κοιλιά':
                    num = '1000'
                int(num)
            except:
                continue

            self.move_mouse(direction.lower(), num)

    def move_mouse(self, direction, num):
        current_x, current_y = pyautogui.position()
        if num != None:
            if '.' in num:
                num = num.replace('.', '')
            # if num.lower().strip() == 'χείλια' or num.lower().strip() == 'κοιλιά':
            #     num = '1000'
            num = int(num)
        else:
            num = 10

        if direction.strip() == 'κάτω':
            new_x = current_x
            new_y = current_y + num
            if new_y > pyautogui.size().height:
                # Scroll the page down if the mouse goes out of sight
                pyautogui.press('down', presses=9)
        elif direction.strip() == 'πάνω' or direction == 'πάνο':
            new_x = current_x
            new_y = current_y - num
            if new_y < 0:
                # Scroll the page up if the mouse goes out of sight
                pyautogui.press('up', presses=9)
        elif direction.strip() == 'δεξιά':
            new_x = current_x + num
            new_y = current_y
        elif direction.strip() == 'αριστερά':
            new_x = current_x - num
            new_y = current_y
        else:
            return  # Invalid direction

        pyautogui.moveTo(new_x, new_y, duration=0.5)