import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pyjokes
import wolframalpha
import requests
import ctypes
import winshell
import time
import json
import cv2
import random
from requests import get
import pywhatkit as kit
import subprocess
import datetime
import pyautogui
import instaloader
import psutil
import pyowm
import urllib.request
from urllib.request import urlopen
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pywikihow import search_wikihow
from twilio.rest import Client
import numpy as np
from PIL import Image
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
def speak(audio):
    engine.say(audio) 
    engine.runAndWait()
print("What Should I Call You?")
print("Give Input From Your KeyBoard")
uname = input("Enter Your Name: ")
print(f"Welcome {uname}")
assistantName =("Pixela")
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("Good Morning")
    elif hour >= 12 and hour < 18:
        print("Good AfterNoon")
    else:
        print("Good Evening")
    print(f"Hello {uname}, I Am {assistantName} your Virtual Assistance, Please tell me How May I help You")
def account_info():
    with open('account_info.txt','r') as f:
        info = f.read().split()
        email = info[0]
        password = info[1]
    return email, password
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('samkrv7@gmail.com','***')
    server.sendmail('samkrv7@gmail.com', to , content)
    server.close()
def date():
    try:
        year = int(datetime.datetime.now().year)
        month = int(datetime.datetime.now().month)
        date = int(datetime.datetime.now().day)
        print(f"The Current Date is {date}-{month}-{year}")
    except Exception as e:
        print("An unknown error has been occurred, Try Again...")
def cpu():
    try:
        usage=str(psutil.cpu_percent())
        print("The CPU Current Usage is " +usage + "Percentage")
    except Exception as e:
        print("An unknown error has been occurred, Try Again...")
def battery():
    try:
        battery = psutil.sensors_battery()
        battery_percentage = str(battery.percent)
        plugged = battery.power_plugged
        print(f"The Battery is {battery_percentage} percent.")
        if plugged:
            print("and It is charging....")
        if not plugged:
            if battery_percentage <= "95%":
                print("Sir, please plug charger.")
    except Exception as e:
        print("An unknown error has been occurred, Try Again...")
def screenshot():
    try:
        print(f"Ok {uname}, Here I Am Going to Take Screenshot...")
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save('D:\\Pixel\\Pixel_Screenshot_Data\\1.png')
    except Exception as e:
        print("An unknown error has been occurred, Try Again...")
def weather_info():
    try:
        owm=pyowm.OWM('eece000de5e319b3c94c04b2d1bc9b15')
        city = pyowm.OWM('eece000de5e319b3c94c04b2d1bc9b15')
        location=owm.weather_at_place(f'{city}')
        weather=location.get_weather()
        temp=weather.get_temperature('celsius')
        humidity=weather.get_humidity()
        date=datetime.datetime.now().strftime("%A:%d:%B:%Y")
        current_temp=temp['temp']
        maximum_temp=temp['temp_max']
        min_temp=temp['temp_min']
        print(f"The Current Temperature on {city} is {current_temp} Degree Celsius ")
        print(f"The Estimated Maximum Temperature for today on {city} is {maximum_temp} Degree Celcius")
        print(f"The Estimated Minimum Temperature for today on {city} is {min_temp} Degree Celcius")
        print(f"The Air is {humidity}% Humid Today")
    except Exception as e:
        print(e)
        print("An unknown error has been occurred, Try Again...")
def current_weather_info():
    try:
        owm=pyowm.OWM('eece000de5e319b3c94c04b2d1bc9b15')
        query = query.replace("weather of", "")
        city = query
        location=owm.weather_at_place(f'{city}')
        weather=location.get_weather()
        temp=weather.get_temperature('celsius')
        humidity=weather.get_humidity()
        date=datetime.datetime.now().strftime("%A:%d:%B:%Y")
        current_temp=temp['temp']
        maximum_temp=temp['temp_max']
        min_temp=temp['temp_min']
        print(f"The Current Temperature on {city} is {current_temp} Degree Celsius ")
        print(f"The Estimated Maximum Temperature for today on {city} is {maximum_temp} Degree Celcius")
        print(f"The Estimated Minimum Temperature for today on {city} is {min_temp} Degree Celcius")
        print(f"The Air is {humidity}% Humid Today")
    except Exception as e:
        print(e)
        print("An unknown error has been occurred, Try Again...")
def givenews():
    apiKey = '49e391e7066c4158937096fb5e55fb5d'
    url = f"https://newsapi.org/v2/top-headlines?country=inio&apiKey={apiKey}"
    r = requests.get(url)
    data = r.json()
    data = data["articles"]
    flag = True
    count = 0
    print(f"=============== TODAY'S TOP 5 HEADLINES ARE ============\n")
    for items in data:
        count += 1
        if count > 5:
            break
        print(items["title"])
        to_print = items["title"].split(" - ")[0]
        if flag:
            print("Today's top 5 Headline are : ")
            flag = False
        else:
            print("Next news :")
        print(to_print)
def tellDay():
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {1: 'Monday', 2: 'Tuesday',  
                3: 'Wednesday', 4: 'Thursday',  
                5: 'Friday', 6: 'Saturday', 
                7: 'Sunday'} 
    if day in Day_dict.keys(): 
        day_of_the_week = Day_dict[day] 
        print(day_of_the_week) 
        print("The day is " + day_of_the_week)
def whatsappMsg(mobNumber,msg,hour,minute,code):
    kit.sendwhatmsg(code+mobNumber,msg,hour,minute)
def OnlineClass(Subject):
    if 'cc' in  Subject:
        Link = "https://meet.google.com/lookup/fyzrp3bvr5?authuser=1&hs=179"
        webbrowser.open(Link)
        time.sleep(10)
        click(x=654, y=344)
        time.sleep(5)
        click(x=716, y=781)
app = wolframalpha.Client("YAAT8K-TGH7575UJ2")
def takeCommand():
    #It takes MicroPhone input from the User and Returns String Output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        print("Listening...")
        r.pause_threshold = 1
        # r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        print("Recognizing...")
        query = r.recognize_google(audio, language = 'en-in')
        print(f"{uname}: {query}\n")
        print("\n")
    except Exception as e:
        print("Unable to Recognize your Voice, Can you Please Repeat...\n")
        return "None"
    return query
if __name__ == "__main__":
    clear = lambda: os.system('cls')
    clear()
    wishMe()
    while True:
        query = takeCommand().lower()
        if 'wikipedia' in query:
            print('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 2)
            print("According to Wikipedia")
            print(results)
        elif 'open youtube' in query:
            print("Here I Am going to Open Youtube")
            print(f"But {uname}, Can You Tell me , What Should I Search On YouTube?")
            search = takeCommand().lower()
            kit.playonyt(f"{search}")
            time.sleep(12)
        elif 'open google' in query:
            print("Here I Am going to Open Google")
            print(f"But {uname}, Can You Tell me , What Should I Search On Google?")
            cm = takeCommand().lower()
            webbrowser.open(f"{cm}")
            time.sleep(8)
        elif 'open stack overflow' in query:
            print("Here I Am going to Open Stack Over flow")
            print(f"But {uname}, Can You Tell me , What Should I Search On Stack Overflow?")
            cm = takeCommand().lower()
            webbrowser.open(f"{cm}")
        elif 'quora' in query:
            print("Here I Am going to Open Quora")
            print(f"But {uname}, Can You Tell me , What Should I Search On Quora?")
            cm = takeCommand().lower()
            webbrowser.open(f"{cm}")
        elif 'open facebook' in query:
            print("Here I Am going to Open FaceBook")
            webbrowser.open("facebook.com")
        elif 'open whatsapp' in query:
            try:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                code = "+91"
                print("Here I Am going to Open WhatsAppWeb")
                print("To Whome You Want To Send Message?")
                print("Give Input From Your KeyBoard")
                mobNumber = int(input("To : "))
                print(f"Ok {uname}, Now Tell Me What Should I Say?")
                msg = takeCommand().lower()
                print("Now You Have To Enter Some Delay Time ...Approx 2 Minute Delay, Because for this Whole Process will take 22 Seconds for Opening WhatsappWeb then 60 Seconds for delivering Message...")
                print("\n")
                print(f"{strTime}")
                print(f"The Current Time is {strTime} and You Have To Enter 2 Minute Approx Delay Time")
                print("Give Input From Your KeyBoard")
                dlyTime = str(input("Delay Time (Example =2:00) = "))
                timeSplit = dlyTime.split(":")
                hour = int(timeSplit[0])
                minute = int(timeSplit[1])
                mobNumber = str(mobNumber)
                msg = str(msg)
                print(f"Ok {uname}, Just Wait...")
                whatsappMsg(mobNumber,msg,hour,minute,code)
                print("Task Completed...")
                time.sleep(3)
            except Exception as e:
                print("An unknown error Has Been occurred, Please Try again")
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"The Time is {strTime}")
        elif 'open camera' in query:
            try:
                vid = cv2.VideoCapture(0) 
                while(True):
                    ret, frame = vid.read()
                    cv2.imshow('frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'): 
                        break;
                vid.release() 
                cv2.destroyAllWindows() 
            except Exception as e:
                print("An unknown error has been occurred, Please Try Again...")
                print("\n")
        elif 'open vs code' in query:
            print(f"Ok {uname}, Here I Am going to open Visual Studio Code")
            codePath = "C:\\Users\\priye\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
        elif 'open notepad' in query:
            print(f"Ok {uname}, Here I Am going to open notepad")
            codePath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(codePath)
        elif 'close notepad' in query:
            print("Here I Am going to close Notepad")
            os.system("task kill /f /im notepad.exe")
            print("\n")
        elif 'open c m d' in query or 'open cmd' in query:
            print(f"Ok {uname}, Here I Am going to open Command Prompt")
            codePath = "C:\\Windows\\system32\\cmd.exe"
            os.startfile(codePath)
        elif 'close c m d' in query or 'close cmd' in query:
            print("Here I Am going to close Command Prompt")
            os.system("taskkill /f /im cmd.exe")
            print("\n")
        elif 'open android studio' in query:
            print(f"Ok {uname}, Here I Am going to open Android Studio")
            codePath = "C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe"
            os.startfile(codePath)    
        elif 'exit' in query or 'bye bye' in query or 'bye' in query or 'get lost' in query:
            print(f"Thanks for using {assistantName}!!!")
            print("\n")
            exit()
        elif 'email to Ananthu' in query:
            try:
                print("What Should I Say?")
                content = takeCommand()
                to = "master.anandhu@gmail.com"
                sendEmail(to, content)
                print("Email Has Been Sent")
                webbrowser.open("mail.google.com")
                time.sleep(20)
            except Exception as e:
                print("An unknown error occurred while sending the email message")
        elif 'send email' in query:
            try:
                print("To Whome Should I Send")
                print("Give Input From Your KeyBoard")
                to = input("To : ")
                print("What Should I Say?")
                content = takeCommand()
                sendEmail(to, content)
                print("Email Has Been Sent")
                webbrowser.open("mail.google.com")
                time.sleep(20)
            except Exception as e:
                print("An unknown error occurred while sending the email message")
        elif 'who are you' in query:
            print(f"I Am {assistantName}, Your Virtual Assistance.")
        elif 'ip address' in query:
            ip = get('https://api.ipiopfy.org').text
            print(f"Sure {uname}, Your Current IP Address is {ip}")
        elif 'how are you' in query:
            print("I Am Happy To Be Here, Thank you")
            print(f"And How are you {uname}")
            Command = takeCommand().lower()
            if 'not fine' in Command:
                print(f"What Happen {uname}?")
                lstCm = takeCommand().lower()
                if 'nothing' in lstCm or 'you will never understand' in lstCm:
                    print(f"Don't be Sad {uname}, Everything will be Alright.")
                else:
                    pass
            elif 'fine' in Command:
                print("It's Good to know that Your Fine")
            else:
                pass
        elif "who made you" in query or "who created you" in query: 
            print("I was Designed or Created by Ananthu S Nair.")
        elif "how old are you" in query or "what is your age" in query:
            print("They Say that, age is nothing just a Number. but Technically, it is also a Word")
        elif 'i love you' in query:
            print(f"I Love You Too {uname}")
        elif 'do you love me' in query:
            print(f"Off Course, I Love You So Much {uname}")
        elif 'how much' in query:
            print("Can't Define in Words How Much I Love You")
        elif 'night' in query:
            print("Nighty Night")
            exit()
        elif 'morning' in query:
            print(f"Good Morning {uname}")
        elif 'afternoon' in query:
            print(f"Good AfterNoon {uname}")
        elif 'evening' in query:
            print(f"Good Evening {uname}")
        elif 'joke' in query:
            try:
                print("Just a Second... Collecting Jokes From Cloud")
                My_joke = (pyjokes.get_joke(language="en", category="neutral"))
                print(My_joke)
            except Exception as e:
                print("An unknown error Has Been occurred, Please Try again")
        elif 'owner mobile number' in query:
            print("My Owner Mobile Number is 89********")
        elif 'who is your owner' in query:
            print("My Owner Name is Ananthu S Nair, And He is a Software Developer.")
        elif 'is love' in query:
            print("It is 7th sense, that destroy all other senses")
        elif 'temperature' in query:
            try:
                print("Just a Second, Fetching Data From Cloud..")
                res = app.query(query)
                print(next(res.results).text)
            except Exception as e:
                print(e)
                print("An unknown error Has Been occurred, Please Try again")
        elif "calculation" in query:
            try:
                print("what Should I Calculate?")
                gh = takeCommand().lower()
                res = app.query(gh)
                print(next(res.results).text)
                print(next(res.results).text)
                time.sleep(1)
            except Exception as e:
                print("An unknown error Has Been occurred, Please Try again")
        elif 'are you ok' in query:
            print(f"Yes {uname}, I Am Ohkay")
            print("And How are you")
            Command = takeCommand().lower()
            if 'not fine' in Command:
                print(f"What Happen {uname}?")
                lstCm = takeCommand().lower()
                if 'nothing' in lstCm or 'you will never understand' in lstCm:
                    print(f"Don't be Sad {uname}, Everything will be Alright.")
                else:
                    pass
            elif 'fine' in Command:
                print("It's Good to know that Your Fine")
            else:
                pass
        elif 'awesome' in query or 'wow' in query or 'amazing' in query or 'wonderful' in query:
            print(f"Thank You {uname}, I Am Always Here To Help You")

        elif 'headlines' in query or 'news' in query or 'headline' in query:
            try:
                print("Sure Sir... Just a Second, Fetching Data From Cloud..")
                givenews()
            except Exception as e:
                print("An unknown error Has Been occurred, Please Try again")
        elif 'thank you' in query:
            print(f"Your Most Welcome {uname}")
        elif 'lock window' in query:
            try:
                print(f"Ok {uname}, Here I Am going to Lock Window")
                print(f"Thanks for using {assistantName}!!!")
                ctypes.windll.user32.LockWorkStation()
                exit()
            except Exception as e:
                print("An unknown error Has Been occurred, Please Try again")
        elif 'shutdown system' in query:
            try:
                print(f"Ok {uname}, Hold a Second ! Your system is on its way to Shut Down")
                print(f"Thanks for using {assistantName}!!!")
                subprocess.call('shutdown / p /f')
                exit()
            except Exception as e:
                print("An unknown error Has Been occurred, Please Try again")
        elif 'stop listening' in query:
            print(f"Ok {uname}, But For How Much time You Want to Stop {assistantName} from listening Commands")
            try:
                timing = takeCommand()
                timing = timing.replace('minutes', '')
                timing = timing.replace('minute', '')
                timing = timing.replace('for', '')
                timing = int(timing)
                timingSec = timing * 60
                timingMin = timingSec // 60
                userprintTime = timingMin
                print(f"Ok {uname}, Here I am going to  Mute Myself for {timingMin} Minutes")
                time.sleep(timingSec)
                print("Time Has Been Finished...")
                print(f"Hello {uname}, I Am {assistantName} your Virtual Assistance, Please tell me How May I help You?")
            except Exception as e:
                print(e)
        elif 'which day it is' in query:
            try: 
                tellDay()
            except Exception as e:
                print("An unknown error Has Been occurred, Please Try again")
        elif 'switch window' in query:
            try:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")
            except Exception as e:
                print("An unknown error Has Been occurred, Please Try again")
        elif 'date' in query:
            date()
        elif 'cpu' in query or 'c p u' in query:
            cpu()
        elif 'battery' in query:
            battery()
        elif 'screenshot' in query or 'ss' in query or 'screenshoot' in query:
            screenshot()
            print("Screenshot Has Been Saved in Our Main Folder")
            time.sleep(2)
        elif 'weather of' in query:
            current_weather_info()
        elif 'weather' in query:
            weather_info()
        elif 'where is' in query or 'Pixel where is' in query:
            query = query.replace("where is ","")
            query = query.replace("Pixel where is ","")
            location = query
            print('Just a Second Sir, Showing you Where is' +location)
            url = 'https://www.google.nl/maps/place/' + location + '/&amp;'
            webbrowser.get().open(url)
            time.sleep(8)
        elif 'internet connection' in query or 'connected to internet' in query:
            hostname="google.co.in"
            response=os.system("ping -c 1" +hostname)
            if response==0:
                print("***...DisConnected...***")
                print("Sir Internet is disconnected")
            else:
                print("***...Connected...***")
                print("Sir you are connected to internet")
        elif 'minimise this window' in query or 'minimize current window' in query or 'minimize this' in query or 'minimise current window' in query:
            try:
                pyautogui.keyDown("win")
                pyautogui.press("down")
                pyautogui.keyUp("win")
                print("Current window has been Minimized")
            except Exception as e:
                print("There Is No Windows to Minimize")
        elif 'maximize this window' in query or 'fullscreen' in query or 'maximise window' in query or 'maximise' in query:
            try:
                pyautogui.keyDown("win")
                pyautogui.press("up")
                pyautogui.keyUp("win")
                print("Current window has been Maximized")
            except Exception as e:
                print("There Is No Windows to Maximize")
        elif 'minimize all windows' in query or 'minimise all' in query or 'minimize all' in query or 'minimize all' in query:
            try:
                os.system('''powershell -command "(new-object -com shell.application).minimizeall()"''')
                print("all windows has been Minimized")
            except Exception as e:
                print("There Is No Windows to Minimize")
        elif 'close current window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("f4")
        elif 'next window' in query:
            print(" Switching to Next Window") 
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")
        elif 'previous window' in query:
            print(" Switching to Previous Window") 
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")
        elif 'timer' in query or 'stopwatch' in query:
            print(f"Ok {uname}, Tell me how many minutes")
            timing = takeCommand()
            timing = timing.replace('minutes', '')
            timing = timing.replace('minute', '')
            timing = timing.replace('for', '')
            timing = int(timing)
            timingSec = timing * 60
            timingMin = timingSec // 60
            userprintTime = timingMin
            print(f"I will remind you in {userprintTime} minutes")
            time.sleep(timingSec)
            print(f"{uname}, Your time has been finished, and we have to start work now")
        elif 'remember' in query:
            print("what should I remember?")
            cm = takeCommand()
            cm = cm.replace(' i ', ' you ')
            cm = cm.replace(' I ', ' you ')
            print(f"You Said Me to Remember that {cm}")
            remember = open('query.txt','w')    
            remember.write(cm)
            remember.close()
        elif 'do you know anything' in query:
            try:
                remember = open('query.txt','r')
                print("you said me to remember that" +remember.read())
            except Exception as e:
                print("you didn't said anything to remember")
        elif 'tell me' in query:
            try:
                max_results = 1
                how_to = search_wikihow(query, max_results)
                assert len(how_to) == 1
                how_to[0].print()
                print(how_to[0].summary)
            except Exception as e:
                print("An unknown error has been occurred, Try Again...")    
        elif 'volume up' in query:
            pyautogui.press("volumeup")
        elif 'volume down' in query:
            pyautogui.press("volumedown")
        elif 'volume mute' in query or 'mute' in query:
            pyautogui.press("volumemute")
        elif 'volume unmute' in query:
            pyautogui.press("volumeunmute")
        elif'mobile camera' in query:
            URL = "http://192.168.14.172:8080/shot.jpg"
            while True:
                img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()),dtype=np.uint8)
                img = cv2.imdecode(img_arr,-1)
                cv2.imshow('IPWebcam',img)
                q = cv2.waitKey(1)
                if q == ord("q"):
                    break;
            cv2.destroyAllWindows()