import os
import subprocess
import eel
import win32com.client
import speech_recognition as sr
import string
import pyttsx3
import webbrowser

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 130)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def get_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not get that")
            print("Sorry, I did not get that")
            return None
        except sr.RequestError:
            speak("Could not request results from Google Speech Recognition service")
            print("Could not request results from Google Speech Recognition service")
            return None

def open_application(app_name):
    shell = win32com.client.Dispatch("WScript.Shell")
    start_menu_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs')
    
    for root, dirs, files in os.walk(start_menu_path):
        for file in files:
            if app_name in file.lower():
                app_path = os.path.join(root, file)
                print(f"Found application shortcut: {app_path}")
                try:
                    shortcut = shell.CreateShortcut(app_path)
                    target_path = shortcut.TargetPath
                    if os.path.exists(target_path):
                        print(f"Opening {target_path}")
                        speak(f"Opening {app_name}")
                        shell.Run(f'"{target_path}"')
                        return True
                    else:
                        print(f"Target path does not exist: {target_path}")
                        speak(f"Target path does not exist for {app_name}")
                except Exception as e:
                    print(f"Failed to open {app_path}: {e}")
                    speak(f"Failed to open {app_name}")
    
    for drive in string.ascii_uppercase:
        drive_path = f"{drive}:\\"
        if os.path.exists(drive_path):
            for root, dirs, files in os.walk(drive_path):
                for file in files:
                    if app_name in file.lower() and file.lower().endswith('.exe'):
                        app_path = os.path.join(root, file)
                        print(f"Found executable: {app_path}")
                        try:
                            print(f"Opening {app_path}")
                            speak(f"Opening {app_name}")
                            subprocess.Popen(app_path)
                            return True
                        except Exception as e:
                            print(f"Failed to open {app_path}: {e}")
                            speak(f"Failed to open {app_name}")

    if webbrowser.open(f"https://www.google.com/search?q={app_name}"):
        return True
    
    return False

def open_file_or_folder(name):
    for drive in string.ascii_uppercase:
        drive_path = f"{drive}:\\"
        if os.path.exists(drive_path):
            for root, dirs, files in os.walk(drive_path):
                for dir in dirs:
                    if name in dir.lower():
                        folder_path = os.path.join(root, dir)
                        print(f"Opening folder: {folder_path}")
                        speak(f"Opening folder {name}")
                        os.startfile(folder_path)
                        return True
                for file in files:
                    if name in file.lower():
                        file_path = os.path.join(root, file)
                        print(f"Opening file: {file_path}")
                        speak(f"Opening file {name}")
                        os.startfile(file_path)
                        return True
                    
    speak(f"Could not find {name} on your computer. Searching the web instead.")
    if webbrowser.open(f"https://www.google.com/search?q={name}"):
        return True
    
    return False
