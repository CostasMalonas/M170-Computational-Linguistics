import SpeechToText as sp
import Browser as br
import time
import pyautogui
import grid as grid
import WORDS as w

class MouseController:
    """
    Κλάση για να μετακινούμε τον mouse cursor, να κάνουμε click, μέσω φωνής να κάνουμε type π.χ σε κάποιο search bar.
    
    Φωνητικές Εντολές:
        1) πάνω - κάτω - αριστερά - δεξιά αριθμός π.χ (δεξιά 100)
            Ο mouse cursor θα μετακινηθεί 100 pixel δεξιά
        2) νέα αναζήτηση 
            Θα πούμε το καινούργιο search term αφού πρώτα το πρόγραμμα μας πεί "Please say your search term"
        3) click - κλίκ (same thing :D)
            Για το mouse click functionality
        4) Όταν το mouse cursor είναι π.χ πάνω από κάποιο search bar και πούμε click και εφανιστεί το cursor
           που υποδικνύει ότι αναμένετε είσοδος από το keyboard, ο χρήστης μπορεί να πεί type και αφού ακουστεί το "Please say what you want to type"
           ο χρήστης λέει αυτό που θέλει να πληκτρολογήσει και πατιέται αυτόματα ENTER αλλιώς μπορεί να πεί delete ή διαγραφή για να διγραφεί 
           οτιδήποτε υπάρχει στο search bar.
    """
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

            if self.text_query.lower() == w.TYPE:
                # Αναμονή για να μιλήσει ο user αφού πεί "type"
                audio_search = sp.obtain_audio_from_mic("Please say what you want to type")
                search_term = sp.convert_speech_to_text(audio_search)
                print(f'search term: {search_term}')

                if search_term != 0:
                    if search_term.lower() == w.DELETE_WORD_1 or w.DELETE_WORD_2 in search_term.lower():
                        # Διαγραγή του τυχόν υπάρχοντος κειμένου στο search bar
                        pyautogui.click(clicks=4)
                        pyautogui.press("backspace")
                        self.search_bar_text = ""
                    else:
                        # Πληκτρολόγηση του term που λέει ο χρήστης στο search bar 
                        pyautogui.typewrite(self.search_bar_text + search_term)
                        self.search_bar_text = self.search_bar_text + search_term
                        pyautogui.press("enter")
                        break
            elif self.text_query.lower() in [w.DELETE_WORD_1, w.DELETE_WORD_2, w.DELETE_WORD_3, w.DELETE_WORD_4]:
                pyautogui.press("backspace", presses=len(self.search_bar_text))
                self.search_bar_text = ""

    def start(self):
        running = True
        while running:
            while True:
                audio_query = sp.obtain_audio_from_mic(w.MESSAGE) # Please say what you want to search
                self.text_query = sp.convert_speech_to_text(audio_query)
                if self.text_query == 0:
                    continue
                else:
                    break

            self.br_obj.perform_google_search(self.text_query)
            if self.num_of_search == 0: # Αν ο χρήστης κάνει αναζήτηση πρώτη φορά accept τα cookies
                self.br_obj.accept_google_cookies()

            while True:
                print('Continued after thread\n')
                audio_query = sp.obtain_audio_from_mic(None)
                time.sleep(2)
                self.text_query = sp.convert_speech_to_text(audio_query)
                print(self.text_query)

                try:
                    query_parts = self.text_query.split()
                except:
                    continue

                if self.text_query.lower() in [w.CLICK_1, w.CLICK_2, w.CLICK_3]:
                    pyautogui.click()  # Εκτέλεσε mouse click
                elif self.text_query.lower() == w.BACK:
                    self.br_obj.driver.back()  # Πήγαινε πίσω στην προηγούμενη σελίδα
                elif self.text_query.lower() == w.TYPE:
                    self.type_in_search_bar()
                elif self.text_query.lower() in [w.OPEN_GRID_1, w.OPEN_GRID_2, w.OPEN_GRID_3, w.OPEN_GRID_4]:
                    grid.grid()
                elif self.text_query.lower() in [w.CLOSE_GRID_1, w.CLOSE_GRID_2, w.CLOSE_GRID_3, w.CLOSE_GRID_4]:
                    grid.close()
                elif self.text_query.lower() == w.NEW_SEARCH:
                    self.num_of_search += 1
                    self.search_bar_text = ""
                    break
                elif query_parts[0].lower() in [w.DOWN, w.DOWN_2, w.LEFT, w.LEFT_2, w.RIGHT, w.RIGHT_2, w.UP_1, w.UP_2, w.UP_3]: # Εντολή μετακίνησης κέρσορα
                    direction = query_parts[0].lower()
                    num = self.parse_number(query_parts[1].lower())
                    self.move_mouse(direction, num)
                elif query_parts[0].lower() == w.SCROLL and len(query_parts) == 3:
                    direction = query_parts[1].lower()
                    amount = self.parse_number(query_parts[2].lower())
                    if direction in [w.DOWN, w.DOWN_2]:
                        pyautogui.scroll(-amount)
                    elif direction in [w.UP_1, w.UP_2, w.UP_3]:
                        pyautogui.scroll(amount)
                elif self.text_query.lower() in [w.EXIT_1, w.EXIT_2]:
                    running = False
                    break

    def parse_number(self, num_str: str):
        # Σε περίπτωση που πει 1000 και το αναγνωρίσει ως "χείλια":
        if num_str == w.THOUSAND_1 or num_str == w.THOUSAND_2:
            return 1000

        num = 0
        if num_str is not None and len(num_str) > 0:
            if '.' in num_str:
                num_str = num_str.replace('.', '')
            try:
                num = int(num_str)
            except ValueError:
                pass

        return num

    def move_mouse(self, direction, num):
        current_x, current_y = pyautogui.position()

        if direction.strip() in [w.DOWN, w.DOWN_2]:
            new_x = current_x
            new_y = current_y + num
            if new_y > pyautogui.size().height:
                # Αν το ποντίκι είναι out of sight -> scroll down
                pyautogui.press('down', presses=9)
        elif direction.strip() in [w.UP_1, w.UP_2, w.UP_3]:
            new_x = current_x
            new_y = current_y - num
            if new_y < 0:
                # # Αν το ποντίκι είναι out of sight -> scroll up
                pyautogui.press('up', presses=9)
        elif direction.strip() in [w.RIGHT, w.RIGHT_2]:
            new_x = current_x + num
            new_y = current_y
        elif direction.strip() in [w.LEFT, w.LEFT_2]:
            new_x = current_x - num
            new_y = current_y
        else:
            return

        pyautogui.moveTo(new_x, new_y, duration=0.5)