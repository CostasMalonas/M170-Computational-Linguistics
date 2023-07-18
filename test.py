"""
Μαλλον θα αρχίσω να δουλέυω σε αυτο το file. Προς το παρόν είναι το file που θα συνεχίσω να δουλεύω.
"""

import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import webbrowser
from word2number import w2n
import test_funs as t

t.browse()
while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        t.speak("Do you want to continue browsing ?")
        audio = r.listen(source)
    try:
        choice = r.recognize_google(audio, language="el-GR")
        print(choice)
        if choice.lower() == "yes":
            t.browse() 
        else:
            break
    except (ValueError, sr.UnknownValueError):
        t.speak("Sorry, please say your choice again")
