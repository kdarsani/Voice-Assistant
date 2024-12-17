import datetime
import json
import sys
import webbrowser
import pyautogui
import pyttsx3
import requests
import speech_recognition as sr
import eel
import time
import wikipedia
from engine.features import *
from engine.open import *

engine = pyttsx3.init()
voices = engine.getProperty('voices')
current_voice_id = 1
current_rate = 130

def speak(text):
    text = str(text)
    engine.setProperty('voice', voices[current_voice_id].id)
    engine.setProperty('rate', current_rate)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

@eel.expose
def switch_voice():
    global current_voice_id
    current_voice_id = 0 if current_voice_id == 1 else 1
    speak(f"Voice switched to {voices[current_voice_id].name}")

@eel.expose
def change_rate(rate_change):
    global current_rate
    current_rate += rate_change
    speak(f"Voice rate set to {current_rate}")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("listening now...")
        print('listening now...')
        eel.DisplayMessage('listening now...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)
    try:
        speak("processing your command...")
        print('processing your command...')
        eel.DisplayMessage('processing your command...')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
    except Exception as e:
        return ""
    return query.lower()

def spell_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 3)
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"user spelled: {query}")
        return query.lower()
    except Exception as e:
        return ""


@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    try:
        if 'no task' not in query:

            if ".com" in query or ".co" in query or ".in" in query or ".org" in query or ".co.in" in query or ".nic.in" in query:
                query = query.replace("open", "").replace("launch", "").replace("nova", "").replace(" ", "")
                speak("opening in browser")
                webbrowser.open(f"https://www.{query}")
                speak("task completed")

                speak("What would you like to do next?")
                allCommands()
                
            if 'open' in query:
                query = query.replace('open', '').strip()
                if 'application' in query:
                    app_name = query.replace('application', '').strip()
                    if not open_application(app_name):
                        speak(f"Could not find an application named {app_name}")
                        print(f"Could not find an application named {app_name}")
                elif 'folder' in query:
                    folder_name = query.replace('folder', '').strip()
                    if not open_file_or_folder(folder_name):
                        speak(f"Could not find a folder named {folder_name}")
                        print(f"Could not find a folder named {folder_name}")
                else:
                    if not open_application(query):
                        if not open_file_or_folder(query):
                            speak(f"Could not find an application or file named {query}")
                            print(f"Could not find an application or file named {query}")

                speak("What would you like to do next?")
                allCommands()


            elif "search on google" in query:
                speak("what should i search on google")
                cm = takecommand().lower()
                webbrowser.open(f"{cm}")
                speak("task completed")

                speak("What would you like to do next?")
                allCommands()

            elif "on youtube" in query:
                from engine.features import PlayYoutube
                PlayYoutube(query)

                speak("What would you like to do next?")
                allCommands()

            elif "wikipedia" in query:
                speak('sure')
                speak('Searching in wikipedia')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("according to wikipedia")
                print(results)
                speak(results)
                speak("Do you have any other queries")

                speak("What would you like to do next?")
                allCommands()

            elif "message" in query or "call" in query or "video call" in query:
                from engine.features import findContact, whatsApp
                flag = ""
                contact_no, name = findContact(query)
                if contact_no != 0:
                    if "message" in query:
                        flag = 'message'
                        speak("what message to send")
                        query = takecommand()
                    elif "phone call" in query:
                        flag = 'call'
                    else:
                        flag = 'video call'
                    whatsApp(contact_no, query, flag, name)
                speak("What would you like to do next?")
                allCommands()

            elif "play my favourite song" in query.lower():
                speak("sure")
                webbrowser.open("https://www.youtube.com/watch?v=1F3hm6MfR1k")
                speak("enjoy your favorite song")

                speak("What would you like to do next?")
                allCommands()

            elif "who created you" in query.lower():
                speak("i am created by Kiran kumar, I am his first AI project.")

                speak("What would you like to do next?")
                allCommands()

            elif "who are you" in query.lower() or "what is your name" in query.lower():
                speak("i am Next-gen operative voice assistant and my name is NOVA")

                speak("What would you like to do next?")
                allCommands()

            elif "time now" in query.lower():
                strtime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Now, the time is {strtime}")

                speak("What would you like to do next?")
                allCommands()

            elif "turn on bluetooth" in query:
                from engine.features import bluetooth
                speak("turning on bluetooth")
                bluetooth()

                speak("What would you like to do next?")
                allCommands()

            elif "turn off bluetooth" in query:
                from engine.features import bluetooth
                speak("turning off bluetooth")
                bluetooth()

                speak("What would you like to do next?")
                allCommands()

            elif "turn on wifi" in query:
                from engine.features import wifi
                speak("turning on wifi")
                wifi()

                speak("What would you like to do next?")
                allCommands()

            elif "turn off wifi" in query:
                from engine.features import wifi
                speak("turning off wifi")
                wifi()

                speak("What would you like to do next?")
                allCommands()

            elif "deactivate" in query:
                speak("Thankyou for your time. deactivating myself")
                pyautogui.hotkey('alt', 'f4')

                speak("What would you like to do next?")
                allCommands()

            elif "volume up" in query:
                pyautogui.hotkey('volumeup')

                speak("What would you like to do next?")
                allCommands()

            elif "volume down" in query:
                pyautogui.hotkey('volumedown')

                speak("What would you like to do next?")
                allCommands()

            elif "mute" in query:
                pyautogui.hotkey('volumemute')

                speak("What would you like to do next?")
                allCommands()

            elif "turn on performance mode" in query:
                pyautogui.hotkey('fn', 'f9')
                speak("performance mode activated")

                speak("What would you like to do next?")
                allCommands()

            elif "turn off performance mode" in query:
                pyautogui.hotkey('fn', 'f9')
                speak("performance mode deactivated")

                speak("What would you like to do next?")
                allCommands()

            elif "today's news" in query:
                def latestnews():
                    api_dict = {
                        "business": "https://gnews.io/api/v4/top-headlines?country=in&category=business&apikey=5fea2c83739de696179b0ca95f675d5b",
                        "entertainment": "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=38beeee34a4e4b7ab4e8275892106462",
                        "health": "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=38beeee34a4e4b7ab4e8275892106462",
                        "science": "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=38beeee34a4e4b7ab4e8275892106462",
                        "sports": "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=38beeee34a4e4b7ab4e8275892106462",
                        "technology": "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=38beeee34a4e4b7ab4e8275892106462"
                    }

                    speak("Which field news do you need: business, health, technology, sports, entertainment, or science?")
                    field = takecommand().lower()

                    url = None
                    for key, value in api_dict.items():
                        if key in field:
                            url = value
                            print("URL was found:", url)
                            break

                    if url is None:
                        speak("Sorry, I couldn't find news in that category. Please choose from business, health, technology, sports, entertainment, or science.")
                        return

                    
                    news = requests.get(url).text
                    news = json.loads(news)
                    speak("Here is the first news.")

                    arts = news.get("articles", [])
                    if not arts:
                        speak("Sorry, no news articles found.")
                        return
                    
                    for articles in arts:
                        article = articles.get("title", "No title available")
                        news_url = articles.get("url", "No URL available")
                        print(article)
                        speak(article)
                        print(f"For more info visit: {news_url}")
                        
                        speak("Do you need more news? Say 'yes' for more or 'no' to stop.")
                        a = takecommand().lower()
                        if "no" in a:
                            break
                        speak("That's all the news for now.")
                
                latestnews()

                speak("What would you like to do next?")
                allCommands()

            elif "weather" in query or "move out" in query or "go out" in query:
                wea(query)

                speak("What would you like to do next?")
                allCommands()

            elif 'text here' in query:
                write_text()

                speak("What would you like to do next?")
                allCommands()

            elif "remember" in query:
                remsg = query.replace('remember','')
                remsg = remsg.replace('nova','')
                remsg = remsg.replace('i ','you')
                speak("you have said to remaind that :"+remsg)
                remember = open('data.txt','w')
                remember.write(remsg)
                remember.close()

            elif "do i have" in query:
                remember = open('data.txt','r')
                remember = remember.replace('have','')
                speak("you have "+ remember.read())


            else:
                from engine.features import chatBot
                comd = query + ". give in two lines"
                chatBot(comd)

                speak("What would you like to do next?")
                allCommands()
    except:
        print("error")
        
    eel.ShowHood()


def wea(query):
    def get_location():
        try:
            response = requests.get('http://ipinfo.io/json')
            data = response.json()
            loc = data['loc'].split(',')
            return loc[0], loc[1]
        except Exception as e:
            print(f"Error getting location: {e}")
            return None, None

    def weather():
        API_KEY = 'bacb834cc85e54f2bf251d01056604d1'
        lat, lon = get_location()
        if lat is None or lon is None:
            speak("Sorry, I couldn't determine your location.")
            return None
        
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
        try:
            response = requests.get(url)
            weather_data = response.json()
            if response.status_code != 200:
                speak("Sorry, I couldn't fetch the weather information.")
                return None
            
            main = weather_data['weather'][0]['main']
            description = weather_data['weather'][0]['description']
            temp = weather_data['main']['temp']
            
            return main, description, temp
        except Exception as e:
            speak("Sorry, I couldn't fetch the weather information.")
            print(f"Error getting weather: {e}")
            return None

    weather_data = weather()
    if weather_data:
        main, description, temp = weather_data
        if "move out" in query:
            if main.lower() in ["rain", "thunderstorm", "snow"]:
                speak(f"The weather is {description} and {temp} degrees Celsius. It is not a good idea to move out right now.")
            else:
                speak(f"The weather is {description} and {temp} degrees Celsius. It seems like a good time to go out.")
        if "go out" in query:
            if main.lower() in ["rain", "thunderstorm", "snow"]:
                speak(f"The weather is {description} and {temp} degrees Celsius. It is not a good idea to move out right now.")
            else:
                speak(f"The weather is {description} and {temp} degrees Celsius. It seems like a good time to go out.")
        elif "weather" in query:
            speak(f"The weather is {description} and {temp} degrees Celsius.")
        else:
            speak("I can provide the weather information if you ask about it.")

def write_text():
    speak("Please spell the text you want to write. Say 'stop' to finish.")
    while True:
        letter = spell_command()
        if letter == 'stop':
            break
        pyautogui.typewrite(letter + ' ')