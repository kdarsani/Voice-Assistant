import sys
import time
import pyttsx3
import speech_recognition as sr
import pickle
import librosa
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
import io
import wave
import noisereduce as nr
from sklearn.ensemble import RandomForestClassifier

from engine.features import playRoboSound

def speak(tex):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 130)
    engine.say(tex)
    engine.runAndWait()

def extract_features(file_name):
    audio, sample_rate = librosa.load(file_name, sr=None)
    audio = nr.reduce_noise(y=audio, sr=sample_rate)
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    delta_mfcc = librosa.feature.delta(mfccs)
    spectral_contrast = librosa.feature.spectral_contrast(y=audio, sr=sample_rate)
    features = np.hstack((np.mean(mfccs.T, axis=0), np.mean(delta_mfcc.T, axis=0), np.mean(spectral_contrast.T, axis=0)))
    
    return features

def record_audio(file_name, duration=5, sample_rate=44100):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Hi, please repeat: 'Hi, Nova, activate.'")
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=duration)

        with io.BytesIO() as buffer:
            buffer.write(audio.get_wav_data())
            buffer.seek(0)
            with wave.open(file_name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(audio.sample_width)
                wf.setframerate(sample_rate)
                wf.writeframes(buffer.read())

def train_model():
    training_files = [
        'engine/samples/sample1.mp3',
        'engine/samples/sample2.mp3',
        'engine/samples/sample3.mp3',
        'engine/samples/sample4.mp3',
        'engine/samples/sample5.mp3',
        'engine/samples/sample6.wav',
        'engine/samples/sample7.wav',
        'engine/samples/sample1.mp3',
        'engine/samples/sample2.mp3',
        'engine/samples/sample3.mp3',
        'engine/samples/sample4.mp3',
        'engine/samples/sample5.mp3',
        'engine/samples/sample6.wav',
        'engine/samples/sample7.wav',
        'engine/samples/sample1.mp3',
        'engine/samples/sample2.mp3',
        'engine/samples/sample3.mp3',
        'engine/samples/sample4.mp3',
        'engine/samples/sample5.mp3',
        'engine/samples/sample6.wav',
        'engine/samples/sample7.wav'
    ]
    negative_files = [
        'engine/samples/negative1.mp3',
        'engine/samples/negative2.mp3',
        'engine/samples/negative3.wav',
        'engine/samples/negative4.wav',
        'engine/samples/negative5.wav',
        'engine/samples/negative6.wav',
        'engine/samples/negative7.wav',
        'engine/samples/negative1.mp3',
        'engine/samples/negative2.mp3',
        'engine/samples/negative3.wav',
        'engine/samples/negative4.wav',
        'engine/samples/negative5.wav',
        'engine/samples/negative6.wav',
        'engine/samples/negative7.wav',
        'engine/samples/negative1.mp3',
        'engine/samples/negative2.mp3',
        'engine/samples/negative3.wav',
        'engine/samples/negative4.wav',
        'engine/samples/negative5.wav',
        'engine/samples/negative6.wav',
        'engine/samples/negative7.wav'
    ]

    features = []
    labels = []

    for file_name in training_files:
        features.append(extract_features(file_name))
        labels.append(1)

    for file_name in negative_files:
        features.append(extract_features(file_name))
        labels.append(0)

    features = np.array(features)
    labels = np.array(labels)

    model = make_pipeline(StandardScaler(), RandomForestClassifier(n_estimators=100, random_state=42))
    model.fit(features, labels)
    with open('voice_auth_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    print("Model trained and saved successfully.")

def authenticate_live(threshold=0.5):
    auth_file = 'live_auth.wav'
    record_audio(auth_file)

    with open('voice_auth_model.pkl', 'rb') as f:
        model = pickle.load(f)

    auth_features = extract_features(auth_file).reshape(1, -1)

    probability = model.predict_proba(auth_features)[0][1]

    print(f"Authentication Probability: {probability}")

    return probability > threshold

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I am hearing now")
        print('I am hearing now...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)

    try:
        speak("Recognizing")
        print('Processing your command...')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        time.sleep(2)
        return query.lower()
    except Exception as e:
        return ""

def validate_password(input_password):
    correct_password = "kiran"
    if input_password == correct_password:
        speak("Password matched. Welcome. Initializing Nova.")
        playRoboSound()
    else:
        speak("Password mismatch. Try again.")
        sys.exit()

def pass_main():
    if authenticate_live():
        print("Voice Authentication successful.")
        speak("Voice Authentication successful. Please provide the password.")
        password_input = take_command()
        print(password_input)
        validate_password(password_input)
    else:
        speak("Voice Authentication failed.")
        sys.exit()

# train_model()


