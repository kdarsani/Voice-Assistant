import pickle
import numpy as np
from sklearn.discriminant_analysis import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from password import extract_features


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
    model = make_pipeline(StandardScaler(), SVC(probability=True, kernel='linear', C=1.0, random_state=42))
    model.fit(features, labels)
    with open('voice_auth_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model trained and saved successfully.")

train_model()