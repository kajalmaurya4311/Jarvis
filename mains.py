# Jarvis is made with ElevenLabs(Text-to-Speech Library)

import speech_recognition as sr
import webbrowser
import musicLibrary
import requests

from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

from apikey import openai_api_key, newsapi, elevenlabs_api_key


# INITIALIZATION

recognizer = sr.Recognizer()

# OpenAI client
openai_client = OpenAI(api_key=openai_api_key)

# ElevenLabs client
elevenlabs = ElevenLabs(api_key=elevenlabs_api_key)


# TEXT TO SPEECH - ELEVENLABS

def speak(text):
    print("Jarvis:", text)

    try:
        audio = elevenlabs.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_flash_v2_5",
            output_format="mp3_44100_128"
        )

        play(audio)

    except Exception as e:
        print("ElevenLabs TTS Error:", type(e).__name__)
        print("Error Details:", repr(e))


# OPENAI AI PROCESSING

def aiProcess(command):

    try:

        completion = openai_client.chat.completions.create(
            model="gpt-5.6-luna",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a virtual assistant named Jarvis. "
                        "You are helpful, intelligent and concise. "
                        "Give short responses because your answers "
                        "will be converted into speech."
                    )
                },
                {
                    "role": "user",
                    "content": command
                }
            ]
        )

        return completion.choices[0].message.content

    except Exception as e:

        print("OpenAI Error:", type(e).__name__)
        print("Error Details:", repr(e))

        return "Sorry, I am unable to process that request right now."


# COMMAND PROCESSING

def processCommand(c):

    command = c.lower().strip()
   
    # GOOGLE
   
    if "open google" in command:

        speak("Opening Google.")

        webbrowser.open("https://google.com")

    # FACEBOOK
   
    elif "open facebook" in command:

        speak("Opening Facebook.")

        webbrowser.open("https://facebook.com")
   
    # YOUTUBE
   
    elif "open youtube" in command:

        speak("Opening YouTube.")

        webbrowser.open("https://youtube.com")


    # PLAY MUSIC
   
    elif command.startswith("play"):

        try:

            words = command.split()

            if len(words) < 2:
                speak("Please tell me which song you want to play.")
                return

            song = words[1]

            if song in musicLibrary.music:

                speak(f"Playing {song}.")

                link = musicLibrary.music[song]

                webbrowser.open(link)

            else:

                speak("Sorry, I could not find that song in your music library.")

        except Exception as e:

            print("Music Error:", type(e).__name__)
            print("Error Details:", repr(e))

            speak("There was a problem playing the song.")


    # NEWS
   
    elif "news" in command:

        try:

            speak("Here are the latest news headlines.")

            url = (
                f"https://newsapi.org/v2/top-headlines"
                f"?country=in&apiKey={newsapi}"
            )

            response = requests.get(url, timeout=10)

            if response.status_code == 200:

                data = response.json()

                articles = data.get("articles", [])

                if not articles:

                    speak("Sorry, I could not find any news right now.")
                    return

                # Read maximum 5 headlines
                for article in articles[:5]:

                    title = article.get("title")

                    if title:
                        speak(title)

            else:

                print("NewsAPI Status Code:", response.status_code)

                try:
                    error_data = response.json()
                    print("NewsAPI Error:", error_data)
                except:
                    pass

                speak("Sorry, I could not fetch the news right now.")

        except requests.exceptions.RequestException as e:

            print("NewsAPI Connection Error:", repr(e))

            speak("I am unable to connect to the news service right now.")


    # AI FALLBACK
   
    else:

        output = aiProcess(c)

        speak(output)


# MAIN PROGRAM

if __name__ == "__main__":

    speak("Initializing Jarvis.")

    while True:

        r = sr.Recognizer()

        print("\n" + "=" * 60)
        print("Recognizing...")
        print("=" * 60)

        try:
          
            # WAIT FOR WAKE WORD
          
            with sr.Microphone() as source:

                print("Listening...")

                audio = r.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=5
                )

            word = r.recognize_google(audio)

            print("You said:", word)


            # CHECK FOR JARVIS WAKE WORD

            if "jarvis" in word.lower():

                print("YES, I heard Jarvis!")

                speak("Yaa")


                # LISTEN FOR COMMAND

                with sr.Microphone() as source:

                    print("Jarvis Active...")
                    print("Speak your command now...")

                    audio = r.listen(
                        source,
                        timeout=5,
                        phrase_time_limit=8
                    )

                command = r.recognize_google(audio)

                print("COMMAND HEARD:", command)

                
                # PROCESS COMMAND
                processCommand(command)


        # ERROR HANDLING

        except sr.WaitTimeoutError:

            print("ERROR: You did not speak within the time limit.")


        except sr.UnknownValueError:

            print("ERROR: Google could not understand what you said.")


        except sr.RequestError as e:

            print(
                "ERROR: Google Speech Recognition service problem:",
                e
            )


        except Exception as e:

            print("ERROR TYPE:", type(e).__name__)
            print("ERROR DETAILS:", repr(e))