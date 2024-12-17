import os
import eel
import datetime

from engine.features import *
from engine.command import *

def start():
    
    eel.init("www")

    def WishMe():
        hour = int(datetime.datetime.now().hour)
        if hour>=0 and hour<12:
            speak("good morning")
        elif hour>=12 and hour<16:
            speak("good afternoon")
        else:
            speak("good evening")
    

    def tellday():
        day = datetime.datetime.today().weekday() + 1
        Day_dict = {1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Saturday',7:'Sunday'}

        if day in Day_dict.keys():
            day_of_the_week = Day_dict[day]
            print (day_of_the_week)
            speak("Today is " + day_of_the_week + ". Have a nice day")

    
    WishMe()
    tellday()

    speak("I am Nova. Activating Myself!!!!")
    playEntrySound()

    os.system('start msedge.exe --app="http://localhost:8000/index.html"')


    eel.start('index.html', mode=None, host='localhost', block=True)
    