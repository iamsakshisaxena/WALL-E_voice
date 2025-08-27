import requests
import json
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random
import speech_recognition as sr
from bs4 import BeautifulSoup
import re
from flask import Flask, render_template

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)


def speak(text):
    engine.say(text)
    engine.runAndWait()

def triggered_by_keyword(command):
    # Use regular expression to check if the trigger word "walle" is present
    return re.search(r'\bwalle\b', command, re.I)

def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!sakshi")
    elif 12 <= hour < 18:
        speak("Good afternoon!sakshi")
    else:
        speak("Good evening!")

    speak("I am wall E. How can I assist you guys today?")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language='en-IN')
        print(f"User input: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand your voice.")
    except sr.RequestError as e:        
        print(f"Request error: {e}")

    return ""
def hi_command(command):
    if 'hello' in command:
        speak('hy miss sakshi.')

def execute_command(command):
    if 'wikipedia' in command:
        speak('Searching Wikipedia...')
        command = command.replace("wikipedia", "")
        results = wikipedia.summary(command, sentences=2)
        speak("According to Wikipedia, ")
        speak(results)
    elif 'open website' in command:
        website = command.replace("open website", "").strip()
        webbrowser.open(website)
    elif 'play' in command:
        song_name = command.replace("play", "").strip()
        play_song_on_youtube(song_name)
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
    elif 'thank you' in command or 'thanks' in command:
        speak("You're welcome!")
    elif 'bye' in command:
        speak("Goodbye!")
        exit()
    elif 'joke' in command:
        joke = get_random_joke()
        speak(joke)
    elif 'quote' in command:
        quote = get_random_quote()
        speak(quote)
    #elif 'weather' in command:
      #  weather = get_current_weather()
       # speak(weather)
    elif 'search' in command:
        search_query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
    elif 'calculate' in command:
        math_expression = command.replace("calculate", "").strip()
        try:
            result = eval(math_expression)
            speak(f"The result is {result}")
        except Exception as e:
            speak("Sorry, I couldn't calculate the expression.")
   
def get_random_joke():
    jokes = ["Why don't scientists trust atoms? Because they make up everything!",
             "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
             "I'm reading a book about anti-gravity. It's impossible to put down!",
             "Why did the scarecrow win an award? Because he was outstanding in his field!",
             "How do you organize a space party? You planet!"]
    return random.choice(jokes)

def get_random_quote():
    quotes = ["The only way to do great work is to love what you do. - Steve Jobs",
              "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
              "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
              "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
              "Believe you can and you're halfway there. - Theodore Roosevelt"]
    return random.choice(quotes)

def get_current_weather():
    api_key = "5d7fa3d3da0ed57ac95f6e2eeef02d82"  
    city = " Noida"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={"5d7fa3d3da0ed57ac95f6e2eeef02d82"}&units=metric"

    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={"5d7fa3d3da0ed57ac95f6e2eeef02d82"}&units=metric")
    data = json.loads(response.text)

    if response.status_code == 200:
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
# return f"The current weather in  Noida sector 62 is {weather}. Temperature is {temperature}°C with {humidity}% humidity."
    #else:
      #  return "Sorry, unable to fetch the weather information at the moment."


def play_song_on_youtube(song_name):
    query = song_name + " song"
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    speak(f"Playing {song_name} on YouTube")

def open_app(app_name):
    app_paths = {
        "notepad":"C:\Windows\notepad.exe",
        "calculator": "calc.exe"
    }
    if app_name in app_paths:
        app_path = app_paths[app_name]
        os.system("./"+app_path)
        speak(f"Opening {app_name}")
    else:
        speak(f"Sorry, I couldn't find the app {app_name}")

if __name__ == "__main__":
    greet()
    while True:
        command = listen()
        if command:
            execute_command(command)