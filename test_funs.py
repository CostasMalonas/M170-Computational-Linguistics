import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import webbrowser
from word2number import w2n
import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


driver = webdriver.Firefox()
driver.maximize_window()

def speak(message):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(message)
    engine.runAndWait()



def accept_google_cookies():
    time.sleep(0.5)
    btn = driver.find_element(By.ID, "L2AGLb")
    btn.click()

def browse():
    # Initialize the speech recognizer
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        speak("Speak your search query:")
        # Listen for the user's input
        audio = r.listen(source)

    # Use Google's speech recognition service to convert the audio to text
    try:
        query = r.recognize_google(audio, language="el-GR")
        print("You said:", query)

        # Perform a Google search with the query
        url = f"https://www.google.com/search?q={query}"
        #webbrowser.open_new_tab(url)
        #headers = {
        #    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
        driver.get(url)
        try:
            accept_google_cookies()
        except:
            print("Cookies already accepted")

        # Parse the search results with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.select(".tF2Cxc")

        # # Print the titles of the top search results
        # print("Top search results:")
        # for i, result in enumerate(results):
        #     print(f"{i+1}.", result.text)

        # Wait for the user to say which search result they want to visit
        while True:
            with sr.Microphone() as source:
                speak("Which search result do you want to visit?")
                audio = r.listen(source)
            try:
                # Convert the audio to text and extract the number of the chosen result
                choice = r.recognize_google(audio, language="el-GR")
                print(choice)
                if choice == "two" or choice == "δύο":
                    choice = 2
                else:
                    choice = int(w2n.word_to_num(choice))
                if choice < 1 or choice > len(results):
                    speak("Please say a number in the range of results")
                    continue
                break
            except (ValueError, sr.UnknownValueError):
                speak(f"Sorry, please say a number between 1 and {len(results)}")
        
        # Open the chosen search result in a new tab
        chosen_result = results[choice - 1]
        chosen_result_url = chosen_result.find("a")["href"]
        print(f"Opening {chosen_result_url} in a new tab...")
        driver.get(chosen_result_url)

        speak("If you want to return say return")
        with sr.Microphone() as source:
            # Listen for the user's input
            audio = r.listen(source)
        # Use Google's speech recognition service to convert the audio to text
        try:
            query_back = r.recognize_google(audio, language="el-GR")
            if query_back.lower() == "return":
                print('URL ', url)
                driver.get(url)
        except:
            pass

    except sr.UnknownValueError:
        speak("Sorry, I could not understand your query.")
    except sr.RequestError as e:
        speak(f"Could not request results from Google Speech Recognition service; {e}")
    except requests.exceptions.RequestException as e:
        speak(f"Could not request results from Google; {e}")
