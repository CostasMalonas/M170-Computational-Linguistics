import Speech_to_Text as sp
import Browser as br
from selenium.webdriver.common.by import By
import time

audio_query = sp.obtain_audio_from_mic("Please say the term you want to search")
text_query = sp.convert_speech_to_text(audio_query)
br_obj = br.Browser()
br_obj.perform_google_search(text_query)
br_obj.accept_google_cookies()

audio_query = sp.obtain_audio_from_mic("Please say the number that indicates the position of the result that you want to visit")
time.sleep(1)
text_query = sp.convert_speech_to_text(audio_query)

while True:
    try:
        text_query = int(text_query)
        print(text_query)
        webelements_ls = br_obj.get_all_google_result_urls()
        url_ls = [elm.find_element(By.TAG_NAME, 'a').get_attribute('href') for elm in webelements_ls]
        br_obj.visit_page(url_ls[text_query])
        break
    except:
        audio_query = sp.obtain_audio_from_mic("Please say the number that indicates the position of the result that you want to visit")
        text_query = sp.convert_speech_to_text(audio_query)
        webelements_ls = br_obj.get_all_google_result_urls()
        print(webelements_ls)

# while text_query.lower() != "exit":
#     while True:
#         sp.perform_google_search(text_query)
#         audio_query = sp.obtain_audio_from_mic("Which of these pages you want to visit ? If you want to exit, say exit.")
#         # Get urls from the result pages
#
#         text_query = sp.convert_speech_to_text(audio_query)
#         if text_query.lower() == "exit":
#             break
#     audio_query = sp.obtain_audio_from_mic("Are you sure you want to exit ? Please say 'exit' to confirm")
#     text_query = sp.convert_speech_to_text(audio_query)

