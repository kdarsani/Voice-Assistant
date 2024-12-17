import csv
import json
from pipes import quote
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import os
import eel
import pyaudio
import pyautogui
from pyautogui import click
import requests
from engine.command import speak, takecommand
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import pvporcupine
from time import sleep
import datetime
import os
import subprocess
import win32com.client
import string

from engine.helper import extract_yt_term, extract_yt_term1, remove_words
from hugchat import hugchat

con = sqlite3.connect("nova.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\www_assets_audio_start_sound.mp3"
    playsound(music_dir)

@eel.expose
def playRoboSound():
    music_dir = "www\\assets\\audio\\robo.mp3"
    playsound(music_dir)

@eel.expose
def playEntrySound():
    music_dir = "www\\assets\\audio\\entry.mp3"
    playsound(music_dir)

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

def PlayYoutube1(query):
    search_term = extract_yt_term1(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    
    try:
        porcupine = pvporcupine.create(keyword_paths=["envzoe\\Lib\\site-packages\\pvporcupine\\resources\\keyword_files\\windows\\hey-nova_en_windows_v3_0_0.ppn"], access_key="e8Rbsh71L8gDr5CGaX6UMEpfFDdMDEfFwEFPgxUU+sq3LpCqJdYtZA==") 
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, 
                                 channels=1, 
                                 format=pyaudio.paInt16, 
                                 input=True, 
                                 frames_per_buffer=porcupine.frame_length)
        
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                print("Custom hotword detected")

                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    if flag == 'message':
        target_tab = 13
        jarvis_message = "message send successfully to "+name
    elif flag == 'call':
        target_tab = 8
        message = ''
        jarvis_message = "calling to "+name
    elif flag == 'video call':
        target_tab = 7
        message = ''
        jarvis_message = "staring video call with "+name

    encoded_message = quote(message)
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
    full_command = f'start "" "{whatsapp_url}"'
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')
    for i in range(1, target_tab):
        pyautogui.hotkey('tab')
    pyautogui.hotkey('enter')
    speak(jarvis_message)

def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response = chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

def bluetooth():
    sleep(1)
    pyautogui.click(x=1699, y=1052)
    sleep(1)
    pyautogui.click(x=1655, y=575)
    sleep(1)
    pyautogui.click(x=1699, y=1052)

def wifi():
    sleep(1)
    pyautogui.click(x=1699, y=1052)
    sleep(1)
    pyautogui.click(x=1518, y=571)
    sleep(1)
    pyautogui.click(x=1699, y=1052)
