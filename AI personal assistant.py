import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests

print('Hey there I am your AI personal assistant - May')

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello, Good Morning")
        print("Hello, Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello, Good Afternoon")
        print("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")
        print("Hello, Good Evening")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said: {statement}\n")
        except Exception as e:
            speak("Pardon me, please say that again")
            return "none"
        return statement.lower()

speak("Hey there I am your AI personal assistant - May")
wishMe()

if __name__ == '__main__':
    while True:
        speak("Tell me how can I help you now?")
        statement = takeCommand()
        if statement == "none":
            continue

        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak('Your personal assistant May is shutting down. Goodbye!')
            print('Your personal assistant May is shutting down. Goodbye!')
            break

        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            try:
                results = wikipedia.summary(statement, sentences=3)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak(f"Disambiguation error: {e.options}")
            except wikipedia.exceptions.PageError:
                speak("Sorry, I could not find a page for that.")

        elif 'open youtube' in statement:
            webbrowser.open("https://www.youtube.com")
            speak("YouTube is open now")
            time.sleep(5)

        elif 'open google' in statement:
            webbrowser.open("https://www.google.com")
            speak("Google Chrome is open now")
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open("https://mail.google.com")
            speak("Google Mail is open now")
            time.sleep(5)

        elif 'time' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am May, version 1.0, your personal assistant. I am programmed to perform tasks such as opening YouTube, Google Chrome, Gmail, and StackOverflow, predicting time, taking photos, searching Wikipedia, getting top headline news from Times of India, and answering computational or geographical questions.')

        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I was built by Medini Sree")
            print("I was built by Medini Sree")

        elif 'news' in statement:
            webbrowser.open("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India. Happy reading!')
            time.sleep(6)

        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0, "robo camera", "img.jpg")

        elif 'search' in statement:
            statement = statement.replace("search", "")
            webbrowser.open(f"https://www.google.com/search?q={statement}")
            time.sleep(5)

        elif 'ask' in statement:
            speak('I can answer computational and geographical questions. What question do you want to ask now?')
            question = takeCommand()
            app_id = "YOUR_APP_ID"  # Replace with your actual WolframAlpha API key
            client = wolframalpha.Client(app_id)
            try:
                res = client.query(question)
                answer = next(res.results).text
                speak(answer)
                print(answer)
            except StopIteration:
                speak("Sorry, I couldn't find an answer to your question.")

        elif "log off" in statement or "sign out" in statement:
            speak("Okay, your PC will log off in 10 seconds. Please make sure you exit all applications.")
            time.sleep(10)
            subprocess.call(["shutdown", "/l"])

        time.sleep(3)
