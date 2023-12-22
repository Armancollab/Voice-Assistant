# A simple voice assistant that can perform basic tasks like setting reminders, creating to-do lists, searching the web and playing music from spotify.
# Author: Arman

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import os
from dotenv import load_dotenv

load_dotenv()

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"User said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't get that.")
            return ""
        except sr.RequestError:
            print("Sorry, I couldn't request results at the moment.")
            return ""


def assistant():
    speak("Hello! How can I help you today?")

    while True:
        command = listen()

        if "set a reminder" in command:
            speak("Sure, what should I remind you about?")
            reminder_text = listen()

            while True:
                speak(
                    "When should I remind you? Please provide the time in HH:MM AM/PM format.")
                reminder_time = listen()

                try:
                    reminder_time = reminder_time.replace(".", "")
                    reminder_time = datetime.datetime.strptime(
                        reminder_time.lower(), "%I:%M %p").time()
                    current_time = datetime.datetime.now().time()

                    if reminder_time >= current_time:
                        speak(
                            f"You want me to remind you about {reminder_text} at {reminder_time.strftime('%I:%M %p')}. Is that correct?")
                        confirmation = listen()

                        if "yes" in confirmation:
                            speak("Reminder set!")
                            break
                        else:
                            speak("Got it, reminder not set.")
                            break

                    else:
                        speak(
                            "The provided time has already passed. Please choose another time.")

                except ValueError:
                    speak(
                        "Invalid time format. Please provide the time in HH:MM AM/PM format. For example, 10:30 AM.")

        elif "create a to-do list" in command:
            speak("Let's create a to-do list. Please start listing tasks.")
            tasks = []
            while True:
                task = listen()
                if "stop" in task or "done" in task:
                    break
                else:
                    tasks.append(task)
            speak("Your to-do list includes:")
            for idx, task in enumerate(tasks):
                speak(f"Task {idx + 1}: {task}")

        elif "search" in command:
            speak("What do you want to search for?")
            search_query = listen()
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(url)
            speak(f"Here are the search results for {search_query}.")

        elif "play music" in command:
            speak("Sure, what music do you want to play?")
            song_name = listen()

            client_id = os.getenv('CLIENT_ID')
            client_secret = os.getenv('CLIENT_SECRET')
            client_credentials_manager = SpotifyClientCredentials(
                client_id=client_id, client_secret=client_secret)
            sp = spotipy.Spotify(
                client_credentials_manager=client_credentials_manager)

            results = sp.search(q=song_name, limit=1)

            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                if track['preview_url']:
                    preview_url = track['preview_url']
                    print(
                        f"Downloading '{track['name']}' by {', '.join([artist['name'] for artist in track['artists']])}")

                    response = requests.get(preview_url)
                    audio_file_path = f'{song_name}.mp3'
                    with open(audio_file_path, 'wb') as f:
                        f.write(response.content)

                    os.startfile(audio_file_path)
                else:
                    print(f"No preview available for '{song_name}'")
            else:
                print(f"No track found for '{song_name}'")

        elif "exit" in command or "bye" in command:
            speak("Goodbye!")
            break

        else:
            speak("I'm sorry, I didn't catch that. Can you repeat again?")


if __name__ == "__main__":
    assistant()
