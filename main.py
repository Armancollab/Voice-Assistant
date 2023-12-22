# A simple voice assistant that can perform basic tasks like setting reminders, creating to-do lists, and searching the web.
# Author: Arman

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
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
            speak(f"I will remind you to {reminder_text} in 5 minutes.")

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

        elif "exit" in command or "bye" in command:
            speak("Goodbye!")
            break

        else:
            speak("I'm sorry, I didn't catch that. Can you repeat again?")


if __name__ == "__main__":
    assistant()
