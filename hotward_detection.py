import pyttsx3
import speech_recognition as sr
import datetime
import os

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e: 
        print("Say that again please...")  
        return "None"
    return query

if __name__ == "__main__":
    while True:
        query = takeCommand().lower()
        if 'wake up Pixel' in query:
            speak("Yes Sir")
            os.startfile('C:\\Users\\priye\\Desktop\\Pixel\\Pixel.py')
        else:
            speak("There is Some Problem with ur Internet Connection")