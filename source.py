import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
import mysql.connector as sql
import random
import pandas as pd

def connection(status):
    if status:
        resp=("Yes! your Connection Estabilished .\n"
              "Now go head to explore your data world ! \n")
        print(resp)
        speak(resp)
        print(commands)
    else:
        print("There is a problem with Data Server, I am unable to reach it.")
        speak("There is a problem with Data Server, I am unable to reach it.")        
        exit(0)
def db_connect():
    try:

        db_connection = sql.connect(host='localhost', database='', user='root', password='ecell123')
        if db_connection:
            return(db_connection)
    except:
        connection(False)

    def db_select():
        rows=show_dbs()
        l=[]
        for i in range(len(rows)):
            l.append(rows[i][0])
        print("Please Select any one of the given databases")
        speak("You can select any one of the given databases")
        return l
    def db_selected():
        rows=db_select()
        for i in range(5):
            dbname=ask()
            if dbname in  rows :
                print("Yes ,", dbname, " Database is in given list !")
                speak("Yes ,"+ dbname + " Database is in given list !")
                break
            else:
                print(dbname, " Not matched in given databases list")
                speak(dbname+ " Not matched in given databases list")

        db_connection2 = sql.connect(host='localhost', database=dbname, user='root', password='ecell123') 
        if db_connection2:
            print("{} Selected. Now you can access the TABLES".format(dbname))
            speak(str(dbname)+ " Selected . Now you can access the TABLES. ")
            return db_connection2, dbname
    def show_tables():
        conn,dtbname=db_selected()
        if conn is not False:
            #global db_connection
                    db_cursor = conn.cursor()    
                    db_cursor.execute('show tables')
                    table_rows1 = db_cursor.fetchall()
                    df1 = pd.DataFrame(table_rows1)
                    speak("Here is the list of Tables available in "+ dtbname+ " Database.")
                    print(df1)
                    return df1.values.tolist(),conn
        else:
                    exit(0)        

    if query == 'connect to database':
        if query not in recorded:
            if db_connect():
                connection(True)
                recorded.append(query)
        else:
            print(' Hey! Cool. I already did that :)- ')
            speak(' Hey! Cool. I already did that !')

    if query == 'show databases':
        show_dbs()
    if query == 'select database':
        db_selected()
    if query == "show tables":
        show_tables()
    if query =='show table data':
        table,conn=show_tables()
        tables=[]
        for i in range(len(table)):
            tables.append(table[i][0])
        print("tables",tables)
        for i in range(5):
            tbname=ask()
            #print(rows)
            if tbname in  tables :
                print("Right! ", tbname, " table is in given list")
                speak("Right! "+tbname+" Table is in given list")
                break
            else:
                print(tbname," Not matched in given Tables list")
                speak(tbname +" Not matched in given Tables list")

        db_cursor = conn.cursor() 
        qry= 'select * from '+tbname
        db_cursor.execute(qry)
        table_rows2 = db_cursor.fetchall()
        df2 = pd.DataFrame(table_rows2)
        speak("Here is the Data of the "+ tbname+" Table available in your database.")
        print(df2)
    return query 


def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

   
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }  
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


instructions = (
        
    )

commands=(
   
    )
print(instructions)
print(commands)
speak(instructions)
#db_connect()
time.sleep(2)

def ask () :
    recognizer1 = sr.Recognizer()
    microphone1 = sr.Microphone()
    for j in range(5):
            speak("I'm Listening ....")
            print("Speak : I'm Listening .... for Table/DB Name ")
            guess = recognize_speech_from_mic(recognizer1, microphone1)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            speak("Sorry. I didn't catch that. What did you say?")
            print("I didn't catch that. What did you say?\n")

       
    if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            exit()
      
    print("You said: {}".format(guess["transcription"]))
    return(guess['transcription'].lower())
if __name__ == "__main__":           
    recorded=[]
    queries=[ 'connect to database',
        'show databases',
        "select database",
        "show tables",
        "show table data"]

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:

        for j in range(5):
            speak("Please Speak. I'm Listening ....")
            print("Speak {}. I'm Listening .... ".format(j+1))
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            speak("Sorry. I didn't catch that. What did you say?")
            print("I didn't catch that. What did you say?\n")

        
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

       
        print("You said: {}".format(guess["transcription"]))

      
        if guess["transcription"] is not None:
            guess_is_correct = guess["transcription"].lower() in queries # "Connect to Database".lower()
            if guess["transcription"].lower()  in ('abort', 'end', 'terminate'):
                speak( " Thanks for Using. Have a Good day !")
                print( " Thanks for Using. Have a Good day !")
                break
        if guess_is_correct:
            txt=query_engine(guess["transcription"]) + " Task Achieved successfuly !"
            print(txt)
            speak(txt)
        else:
            print("Sorry, I can't perform what you have said . Please try again! ")#.format(word))
            speak("Sorry, I can't perform what you have said . Please try again!")