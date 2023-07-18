import speech_recognition as sr
import webbrowser
import pyttsx3

def speak(message):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(message)
    engine.runAndWait()


def obtain_audio_from_mic(message):
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if message != None:
            speak(message)
        audio = r.listen(source)
    return audio


def convert_speech_to_text(audio):
    try:
        r = sr.Recognizer()
        query = r.recognize_google(audio, language="el-GR")
        #speak(query)
        return query
    except sr.UnknownValueError:
        return 0


def perform_google_search(query):
    # perform Google search
    url = "https://www.google.com/search?q=" + query
    webbrowser.open_new(url)


# def convert_speech_to_text_for_mouse(audio):
#     try:
#         r = sr.Recognizer()
#         query = r.recognize_google(audio, language="el-GR")
#         #speak(query)
#         return query
#     except sr.UnknownValueError:
#         return 0