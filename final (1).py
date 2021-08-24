#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install SpeechRecognition
import datetime
import wikipedia #pip install wikipedia
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   
    elif hour>=18 and hour<=24:
        speak("Good Evening!")
    else:
        speak("Good Night!")  

    speak("Hello I am Ester  , How can I help you")       

def takeCommand():
    #It takes microphone input from the user and returns string output

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
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def gen_labels():
        labels = {}
        with open("labels.txt", "r") as label:
            text = label.read()
            lines = text.split("\n")
            for line in lines[0:-1]:
                    hold = line.split(" ", 1)
                    labels[hold[0]] = hold[1]
        return labels

if __name__ == "__main__":
    wishMe()
    while True:
     #if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'can you find' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)
      
        elif 'identify me' and 'find me' in query:
            np.set_printoptions(suppress=True)
            model = load_model('keras_model.h5')
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            image = Image.open('http://localhost:8888/view/Downloads/Untitled%20Folder/image%201.jpg')
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.ANTIALIAS)
            image_array = np.asarray(image)
            image.show()
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image_array
            prediction = model.predict(data)
            result = np.argmax(prediction[0])
            print(prediction)
            speak ("prediction is ")
            print(gen_labels()[str(result)])
            speak(gen_labels()[str(result)])
            
           # if prediction<=50 :
               # speak("couldnt recoqnize you")
            
     


# In[ ]:




