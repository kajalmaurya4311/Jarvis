# Jarvis is made with pyttsx3 & gtts (Text-to-Speech Library) 

import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
from apikey import openai_api_key, newsapi

# recognizer recognize when we speak something
recognizer = sr.Recognizer()

# speak function convert text to speech
def speak_old(text):
    engine = pyttsx3.init()
    engine.setProperty("volume", 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")    
    

    
def aiProcess(command):
    client = OpenAI(api_key = openai_api_key,
    )

    completion = client.chat.completions.create(
        model="gpt-6-astra",
        messages=[
            {"role": "system", "content": "You are a Virtual assistant named jarvis skilled in general tasks like ALexa and Google Cloud.Give short responses please."},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content
   

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link =  musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            # Extract the articles
            articles = data.get('articles', [])
            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)

    
if __name__ == "__main__":
    speak("Initializing jarvis......")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
        print("Recognizing....")
        
        try:

            # Listen for wake word
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(
                    source, timeout=5, phrase_time_limit=5)
                    
            # Recognize wake word
            word = r.recognize_google(audio)
            print("You said:", word)

            if "jarvis" in word.lower():
                print(" YES, I heard Jarvis! Attempting to speak now...")
                speak("Yaa")

                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active....")
                    print("Speak your command now...")

                    audio = r.listen(
                        source, timeout=5, phrase_time_limit=5)
                        
                # Recognize command
                command = r.recognize_google(audio)
                print(" COMMAND HEARD:", command)

                processCommand(command)

        except sr.WaitTimeoutError:
            print("ERROR: You did not speak within the time limit.")

        except sr.UnknownValueError:
            print("ERROR: Google could not understand what you said.")

        except sr.RequestError as e:
            print("ERROR: Google Speech Recognition service problem:", e)

        except Exception as e:
            print("ERROR TYPE:", type(e).__name__)
            print("ERROR DETAILS:", repr(e))


