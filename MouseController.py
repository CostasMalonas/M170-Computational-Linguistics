import SpeechToText as sp
import Browser as br
import time
import pyautogui
import grid as grid
from threading import Thread

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

            if self.text_query.lower() == "type":
                # Αναμονή για να μιλήσει ο user αφού πεί "type"
                audio_search = sp.obtain_audio_from_mic("Please say what you want to type")
                search_term = sp.convert_speech_to_text(audio_search)
                print(f'search term: {search_term}')

                if search_term != 0:
                    if search_term.lower() == "delete" or 'lidl' in search_term.lower():
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
            elif self.text_query.lower() in ["delete", "elite", "διαγραφή"]:
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
            print('Continued after thread\n')
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
                    pyautogui.click()  # Εκτέλεσε mouse click
                elif self.text_query.lower() == 'πίσω':
                    self.br_obj.driver.back()  # Πήγαινε πίσω στην προηγούμενη σελίδα
                elif self.text_query.lower() == 'type':
                    self.type_in_search_bar()
                elif 'open' in self.text_query.lower():
                    print('HEEEEEERE')
                    thread = Thread(grid.grid()) # Σημείωση: να το κάνω με threads
                    thread.start()
                elif 'close' in self.text_query.lower():
                    grid.close()
                    #pyautogui.click()
                continue  # Αν query_parts != 2 πήγαινε στην αρχή του loop

            if self.text_query.lower() == 'νέα αναζήτηση':
                self.num_of_search = 1
                self.search_bar_text = ""
                self.start()  # Πραγματοποίησε νέα αναζήτηση 



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
                # Αν το ποντίκι είναι out of sight -> scroll down
                pyautogui.press('down', presses=9)
        elif direction.strip() == 'πάνω' or direction == 'πάνο':
            new_x = current_x
            new_y = current_y - num
            if new_y < 0:
                # # Αν το ποντίκι είναι out of sight -> scroll up
                pyautogui.press('up', presses=9)
        elif direction.strip() == 'δεξιά':
            new_x = current_x + num
            new_y = current_y
        elif direction.strip() == 'αριστερά':
            new_x = current_x - num
            new_y = current_y
        else:
            return

        pyautogui.moveTo(new_x, new_y, duration=0.5)