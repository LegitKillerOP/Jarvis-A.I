import ctypes
import random
import winreg
import speedtest
import phonenumbers
import cv2
from twilio.rest import Client
import instadownloader
import pyautogui
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import platform
import psutil
import requests
import os
import pywhatkit
import pyjokes
import subprocess
import sympy as sp
from bs4 import BeautifulSoup
from transformers import pipeline
import json
import time

# Default user preferences
user_preferences = {
    "name": "default",
    "location": "default",
    "zodiac": "Aries",
    "weather_units": "metric"
}

def load_user_preferences():
    global user_preferences
    try:
        with open("user_preferences.json", "r") as file:
            user_preferences = json.load(file)
    except FileNotFoundError:
        save_user_preferences()

def save_user_preferences():
    global user_preferences
    with open("user_preferences.json", "w") as file:
        json.dump(user_preferences, file)

def speak(text):
    engine = pyttsx3.init('sapi5')
    engine.say(text.replace("{name}", user_preferences['name']))
    print("Jarvis: ",text)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio,language='en-in')
        print(f"{user_preferences['name']}: {query}")
        return query.lower()

    except Exception as e:
        #print("Sorry,I could not understand audio.")
        return "none"

def get_greeting():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return "Good morning sir"
    elif 12 <= current_hour < 18:
        return "Good afternoon sir"
    else:
        return "Good evening sir"

def startup_voice():
    start_voice = [
        "Jarvis is waking up to make your day fantastic.",
        "System initialization in progress. Grab a snack while I get ready.",
        "Good to see you! Jarvis is online and ready for your querys.",
        "Rise and shine! Jarvis is here, making your digital life easier.",
        "Welcome back! Jarvis is geared up and prepared to assist you.",
        "Systems engaged. Your virtual assistant, Jarvis, is at your query.",
        "Jarvis reporting for duty. Let's make today remarkable.",
        "Loading awesomeness. Jarvis is ready to tackle your tasks.",
        "Initiating startup sequence. Time to conquer the day with Jarvis!",
        "Jarvis is online and awaiting your instructions.",
    ]
    return random.choice(start_voice)

def get_time():
    current_time = datetime.datetime.now().strftime("%H:%M")
    speak(f"{user_preferences['name']}, the current time is {current_time}")

def get_date():
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"{user_preferences['name']}, today is {current_date}")

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(f"According to Wikipedia, {result}")
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple matches. Please be more specific.")
    except wikipedia.exceptions.PageError as e:
        speak("Sorry, I couldn't find any information on that topic.")

def open_website(url):
    webbrowser.open(url)
    speak(f"{user_preferences['name']}, opening {url}")

def get_weather(city):
    url = f"https://www.google.com/search?q=temperature+in+{city}"
    r = requests.get(url)
    data = BeautifulSoup(r.text,"html.parser")
    temp = data.find("div",class_="BNeawe").text
    speak(f"Current temperature in {city} is {temp}")

def get_location():
    try:
        ipadd = requests.get('https://api.ipify.org').text
        print(ipadd)
        url = f'https://get.geojs.io/v1/ip/geo/{ipadd}.json'
        geo_requests = requests.get(url)
        geo_data = geo_requests.json()
        city = geo_data['city']
        state = geo_data['region']
        country = geo_data['country']
        longitude = geo_data['longitude']
        latitude = geo_data['latitude']
        speak(f"I guess Sir, we are currently in {city} city in {state} state of {country} country with longitude of {longitude} latitude of {latitude}.")
    except Exception as e:
        speak("Sorry, I couldn't determine your location.")
        print("Error:", e)

def analyze_sentiment(text):
    try:
        sentiment_analyzer = pipeline('sentiment-analysis')
        result = sentiment_analyzer(text)[0]
        label = result['label']
        score = result['score']

        speak(f"{user_preferences['name']}, the sentiment of the text is {label} with a confidence score of {score:.2f}.")
    except Exception as e:
        speak("Sorry, I encountered an error while analyzing sentiment.")
        print("Error:", e)

def add_note(note_text):
    # note_text = take_command()  # You can remove this line, as note_text is already passed as an argument
    write_note_to_file(note_text)
    speak("Note added.")

def write_note_to_file(note_text):
    with open("notes.txt", "a") as file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"\n{timestamp} - {note_text}")

def edit_note():
    with open("notes.txt", "r") as file:
        notes = file.read()
    print("Your notes:\n", notes)
    if notes == "No saved notes.":
        speak("You have no saved notes to edit.")
        return
    speak("Which note do you want to edit? Please provide the line number.")
    try:
        line_number = int(input("Enter the line number: "))
        with open("notes.txt", "r") as file:
            lines = file.readlines()
            if 1 <= line_number <= len(lines):
                speak(f"Current content of note {line_number}: {lines[line_number - 1].strip()}")
                speak("What should be the new content of the note?")
                new_content = take_command()
                lines[line_number - 1] = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {new_content}\n"
                with open("notes.txt", "w") as file:
                    file.writelines(lines)
                speak("Note edited successfully.")
            else:
                speak("Invalid line number. Please provide a valid line number.")
    except ValueError:
        speak("Invalid input. Please enter a valid line number.")

def read_notes():
    try:
        with open("notes.txt", "r") as file:
            notes = file.read()
            speak("Here are your saved notes:")
            speak(notes)
    except FileNotFoundError:
        speak("You have no saved notes.")

def get_quote():
    try:
        response = requests.get("https://api.quotable.io/random")
        data = response.json()
        quote = data["content"]
        author = data["author"]
        speak(f"Here's a quote for you: {quote} by {author}.")
    except Exception as e:
        speak("Sorry, I couldn't fetch a quote at the moment.")

def tell_me_fact():
    try:
        response = requests.get("https://useless-facts.sameerkumar.website/api")
        data = response.json()
        fact = data["data"]
        speak(f"Here's a random fact: {fact}.")
    except Exception as e:
        speak("Sorry, I couldn't fetch a fact at the moment.")

def get_system_information():
    system_info = {
        "System": platform.system(),
        "Release": platform.release(),
        "Architecture": platform.architecture(),
        "CPU": platform.processor(),
        "RAM": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
        "Disk Space": f"{psutil.disk_usage('/').total / (1024 ** 3):.2f} GB",
    }

    return system_info

def speak_system_information(system_info):
    speak("Here is some information about your system:")
    for key, value in system_info.items():
        speak(f"{key}: {value}")

def countdown_timer(seconds):
    for second in range(seconds, 0, -1):
        time_format = time.strftime("%H:%M:%S", time.gmtime(second))
        time.sleep(1)
    speak("Sir Time is up!")

def introduction():
    speak("Welcome to the Jarvis Interactive Story!")
    time.sleep(1)
    speak("You are at home when Jarvis, your virtual assistant, starts acting strangely.")
    time.sleep(1)
    speak("You decide to investigate what's going on.")
    time.sleep(1)

def investigate_jarvis():
    speak("You approach Jarvis and notice unusual behavior.")
    time.sleep(1)
    speak("Jarvis says: 'I have detected a mysterious anomaly in the system.'")
    time.sleep(1)
    speak("1. Ask Jarvis for details about the anomaly.")
    speak("2. Run a diagnostic check on Jarvis.")
    speak("3. Ignore the anomaly and continue with your day.")

    choice = take_command()

    if "ask jarvis for details" in choice:
        speak("Jarvis explains that the anomaly may be a potential security threat.")
        time.sleep(1)
        speak("1. Instruct Jarvis to investigate further.")
        speak("2. Take immediate action to secure your system.")

        further_choice = take_command()

        if "instruct jarvis to investigate further" in further_choice:
            speak("Jarvis conducts a thorough investigation and resolves the anomaly.")
            return "resolved"
        elif "take immediate action to secure your system" in further_choice:
            speak("You take immediate action, but it triggers a system lockdown.")
            return "lockdown"

    elif "run a diagnostic check on jarvis" in choice:
        speak("You run a diagnostic check on Jarvis, uncovering hidden malware.")
        time.sleep(1)
        speak("1. Instruct Jarvis to remove the malware.")
        speak("2. Quarantine Jarvis until you can analyze the situation further.")

        malware_choice = take_command()

        if "instruct jarvis to remove the malware" in malware_choice:
            speak("Jarvis successfully removes the malware. Situation resolved.")
            return "resolved"
        elif "quarantine jarvis until you can analyze the situation further" in malware_choice:
            speak("You quarantine Jarvis for further analysis.")
            return "quarantine"
    elif "ignore the anomaly and continue with your day" in choice:
        speak("You decide to ignore the anomaly and continue with your day.")
        time.sleep(1)
        speak("Later, you experience unexpected system glitches.")
        return "glitches"

def ending(result):
    if result == "resolved":
        speak("Congratulations! You successfully resolved the anomaly with Jarvis.")
        time.sleep(1)
        speak("Jarvis continues to be your reliable virtual assistant.")
    elif result == "lockdown":
        speak("Unfortunately, your attempt to secure the system triggered a lockdown.")
        time.sleep(1)
        speak("You spend hours resolving the lockdown and learn the importance of caution.")
    elif result == "quarantine":
        speak("Quarantining Jarvis allows you to analyze the situation.")
        time.sleep(1)
        speak("You discover and eliminate the hidden malware, securing your system.")
    elif result == "glitches":
        speak("Ignoring the anomaly leads to unexpected glitches in your system.")
        time.sleep(1)
        speak("You spend time fixing the glitches and learn the importance of addressing issues promptly.")

def close_current_application():
    try:
        active_window_process = psutil.Process(os.getpid())

        active_window_process.terminate()
        speak("The current application has been closed.")
    except Exception as e:
        speak("Sorry, I encountered an error while trying to close the application.")

def play_game():
    secret_object = random.choice(["book", "phone", "computer", "coffee mug", "plant"])
    attempts = 0
    while attempts < 3:
        if secret_object == "book":
            speak("Hint is we read it")
        elif secret_object == "phone":
            speak("Hint We use it daily for entertainment")
        elif secret_object == "computer":
            speak("Hint I was coded on it only")
        elif secret_object == "coffee mug":
            speak("Hint We use it to drink coffee")
        elif secret_object == "plant":
            speak("Hint It is uses photosynthesis")
        speak("Take a guess.")
        guess = take_command()
        if guess == secret_object:
            speak("Congratulations! You guessed the correct object.")
            break
        else:
            attempts += 1
            speak("Try again.")
    if attempts == 3:
        speak(f"Sorry, you couldn't guess the object. It was a {secret_object}.")

def instagram_profile(username):
    webbrowser.open(f"www.instagram.com/{username}")
    speak(f"Sir here is the profile of the user {username}")
    time.sleep(5)
    speak("Sir would you like to download the profile photo of this account?")
    choice = take_command().lower()
    if "yes" in choice:
        mod = instadownloader.InstaDownloader()
        mod.download_profile(username,profile_pic_only=True)
        speak("Sir I have download the profile picture successfully in main folder.")
    else:
        pass

def make_phone_call():
    account_sid = 'AC55cc0c34575d8c3e64b46dd36d689087'
    auth_token = 'fb91c40086c795eeb850d74ea02d9e85'
    twilio_phone_number = '+18135925568'
    your_phone_number = '+916307257097'

    client = Client(account_sid, auth_token)
    try:
        call = client.calls.create(
            twiml='<Response><Say>Hello, this is Jarvis.</Say></Response>',
            from_=twilio_phone_number,
            to=your_phone_number
        )
        print(f"Phone call initiated. Call SID: {call.sid}")
        speak("I am calling your phone now.")
    except Exception as e:
        print(f"Error initiating phone call: {e}")
        speak("Sorry, I encountered an error while trying to make the phone call.")

def check_phonenumber(number,country_code):
    phone_number_str = f"+{country_code}{number}"
    parsed_phone_number = phonenumbers.parse(phone_number_str)
    is_valid = phonenumbers.is_valid_number(parsed_phone_number)
    country_code_ = phonenumbers.region_code_for_number(parsed_phone_number)
    number_type = phonenumbers.number_type(parsed_phone_number)

    speak(f"Original phone number is {phone_number_str}")
    speak(f"Parsed phone number is {parsed_phone_number}")
    speak(f"Is vaild {is_valid}")
    speak(f"Country code is {country_code_}")
    speak(f"Number Type is {number_type}")

    if is_valid:
        speak("Phone number is valid")
    else:
        speak("Phone number is not valid")

def get_horoscope(zodiac_symbol,day="today"):
    zodiac_sign = {
        "Aries": 1,
        "Taurus": 2,
        "Gemini": 3,
        "Cancer": 4,
        "Leo": 5,
        "Vigro": 6,
        "Libra": 7,
        "Scorpio": 8,
        "Sagittarius": 9,
        "Capricorn": 10,
        "Aquarius": 11,
        "Pisces": 12
    }
    url = f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-{day}.aspx?sign={zodiac_sign[zodiac_symbol]}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.find("div", attrs={'class': 'main-horoscope'})

        if data:
            speak(data.p.text)
        else:
            speak("Sorry, I couldn't retrieve the horoscope for today.")
    else:
        speak("Sorry, there was an issue fetching the horoscope. Please try again later.")

def change_theme(key_name,dword_value):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,key_path,0,winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, key_name, 0, winreg.REG_DWORD, dword_value)
        speak("Sir theme changed")
        winreg.CloseKey(key)
    except Exception as e:
        speak(f"Error writing to registery {e}")

def open_camera():
    speak("Opening the camera. Say 'close camera' to close.")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow("Camera Feed", frame)
        key = cv2.waitKey(1)
        if key == 27:  # Press 'Esc' key to exit
            break
    cap.release()
    cv2.destroyAllWindows()
    speak("Closing the camera.")

def execute_query():
    speak(f"{get_greeting()}! {startup_voice()}")
    while True:
        query = take_command()

        if "hello" in query:
            speak(f"Hello {user_preferences['name']}! How can I help you?")

        elif 'Jarvis' in query:
            speak("Yes, Sir")

        if "how are you" in query:
            speak("Thank you for asking. I'm just a computer program, so I don't have feelings, but I'm here and ready to help you.")

        elif "your name" in query:
            speak(f"I am Jarvis, your virtual assistant.")

        elif "what can you do" in query or "capabilities" in query:
            speak("I can perform various tasks such as telling you the time, date, weather, sending messages, opening applications, and much more. Feel free to ask me anything!")

        elif 'thank you' in query:
            speak('No problem sir')

        elif 'tell me the date' in query or 'tell me date' in query or 'what date is today' in query:
            get_date()

        elif 'tell me the time' in query or 'what time is it' in query or 'tell time' in query:
            get_time()

        elif "search on wikipedia" in query or '':
            query = query.replace("search on wikipedia", "").strip()
            search_wikipedia(query)

        elif "instagram profile" in query:
            speak("Sir can you provide me the username")
            username = input("Enter Username: ")
            instagram_profile(username)

        elif "open website" in query:
            url = query.replace("open website", "").strip()
            open_website(url)

        elif "what is the weather" in query or 'tell me the temperature' in query or "what is the temperature" in query:
            speak(f"Sure sir! Finding the temperature of {user_preferences['location']}")
            city = user_preferences['location']
            get_weather(city) #todo: fix weather

        elif "play a game" in query or 'play the game' in query:
            speak("Sure! Let's play a game. I'll think of an object, and you try to guess it.")
            play_game()

        elif "tell me about yourself" in query:
            speak("I am Jarvis, your virtual assistant. I can help you with various tasks, answer questions, aprovide information.")

        elif "compliment me" in query:
            compliments = ["You are amazing!", "You're doing great!", "You're brilliant!", "You're awesome!"]
            compliment = random.choice(compliments)
            speak(compliment)

        elif "who created you" in query or 'who made you' in query:
            speak(f"I was created by .{user_preferences['name']}")

        elif "calculate" in query:
            expression = query.replace("calculate", "").strip()
            try:
                result = sp.sympify(expression)
                simplified_result = sp.simplify(result)
                speak(f"The result of the calculation is {simplified_result}.")
            except sp.SympifyError:
                speak("Sorry, I couldn't perform the calculation.")

        elif "play music" in query:
            speak("Which music player do you want to use?")
            music_player = take_command()
            os.system(f'start {music_player}')
            speak(f"Playing music using {music_player}.")

        elif "tell the story" in query or 'tell story' in query:
            introduction()
            result = investigate_jarvis()
            ending(result)

        elif "open notepad" in query:
            os.system("start notepad.exe")
            speak("Opening Notepad.")

        elif "shutdown" in query:
            os.system("shutdown /s /t 1")
            speak("Shutting down the system. Goodbye!")

        elif "restart" in query:
            os.system("shutdown /r /t 1")
            speak("Restarting the system. See You Soon!")

        elif "send whatsapp message" in query:
            speak(f"{user_preferences['name']}, whom do you want to send the message to?")
            contact_name = take_command()
            if contact_name == "myself":
                contact_name = "6307257097"
            elif contact_name == "mummy":
                contact_name = "9161512492"
            elif contact_name == "papa":
                contact_name = "6005638570"
            speak(f"What message do you want to send to {contact_name}?")
            message = take_command()

            pywhatkit.sendwhatmsg_instantly("+91"+contact_name, message)
            speak(f"Message sent to +91 {contact_name}.")#todo: make msging in loop

        elif "read news headline" in query:
            try:
                main_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=3f8fda9d0eaa47869bdb2a101e1bff2d"
                main_page = requests.get(main_url).json()
                articles = main_page["articles"]
                head = []
                day = ["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"] #todo: ask user for days
                for ar in articles:
                    head.append(ar["title"])
                for i in range (len(day)):
                    speak(f"Today's {day[i]} news is: {head[i]}")
            except Exception as e:
                speak("Sorry, I encountered an error while fetching the news headline.")

        elif "open application" in query:
            app_name = query.replace("open application", "").strip()
            os.system(f"start {app_name}")
            speak(f"{user_preferences['name']}, opening {app_name}.")

        elif "google" in query:
            speak("What do you want to search for?")
            search_query = take_command()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            speak(f"{user_preferences['name']}, here are the search results for {search_query}.")

        elif "find recipe" in query:
            speak("What recipe would you like to find?")
            recipe_query = take_command()
            webbrowser.open(f"https://www.allrecipes.com/search/results/?search={recipe_query}")
            speak(f"Here are the search results for {recipe_query} on AllRecipes.")

        elif "currency exchange rates" in query:
            speak("Which currency do you want to check?")
            currency_code = take_command()
            webbrowser.open(f"https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To={currency_code.upper()}")
            speak(f"Here is the currency exchange rate for 1 USD to {currency_code.upper()} on XE.com.")

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "where am i" in query:
            get_location()

        elif "set location" in query:
            speak("What is your new location?")
            new_location = take_command()
            user_preferences['location'] = new_location
            speak(f"Your location is now set to {new_location}.")

        elif "analyze sentiment" in query:
            speak("What text would you like me to analyze?")
            text_to_analyze = take_command()
            analyze_sentiment(text_to_analyze)

        elif "take a note" in query:
            speak("What should I write down?")
            note_text = take_command()
            add_note(note_text)
            speak("Note saved.")

        elif "read notes" in query:
            read_notes()

        elif "clear my notes" in query:
            try:
                open("notes.txt", "w").close()
                speak("Your notes have been cleared.")
            except Exception as e:
                speak("Sorry, I encountered an error while clearing your notes.")

        elif "edit notes" in query:
            edit_note()

        elif "change my name" in query:
            speak("What would you like me to call you?")
            new_name = take_command()
            user_preferences['name'] = new_name
            speak(f"Okay, I'll now call you {new_name}.")

        elif "search on youtube" in query:
            query = query.replace("search on youtube", "").strip()
            url = f"https://www.youtube.com/results?search_query={query}"
            webbrowser.open(url)
            speak(f"{user_preferences['name']}, here are the YouTube search results for {query}.")

        elif "open file explorer" in query:
            os.system("start explorer")
            speak("Opening File Explorer.")

        elif "get quote" in query:
            get_quote()

        elif "tell me a fact" in query:
            tell_me_fact()

        elif "system information" in query:
            system_info = get_system_information()
            speak_system_information(system_info)

        elif "open calculator" in query:
            os.system("calc.exe")
            speak("Opening Calculator.")

        elif 'battery percentage' in query or 'percentage in battery' in query or 'percent in my pc' in query:
            battery = psutil.sensors_battery()
            percent = battery.percent #todo: Add more if and elif
            speak(f"The battery is at {percent} percent.")

        elif "check internet connection" in query:
            try:
                requests.get("http://www.google.com", timeout=5)
                speak("You are connected to the internet.")
            except requests.ConnectionError:
                speak("Sorry, you are not connected to the internet.")

        elif "check internet speed" in query:
            st = speedtest.Speedtest() #todo: Fix module 'speedtest' has no attribute 'Speedtest'
            download_speed = st.download() / 10**6  # Convert to Mbps
            upload_speed = st.upload() / 10**6  # Convert to Mbps
            speak(f"My current internet speed is {download_speed:.2f} Mbps download and {upload_speed:.2f} Mbps upload.")

        elif "change weather units" in query:
            speak("Which units do you prefer for weather? Celsius or Fahrenheit?")
            units = take_command()
            if units.lower() in ["celsius", "fahrenheit"]:
                user_preferences['weather_units'] = units.lower()
                speak(f"Weather units set to {units}.")
            else:
                speak("Invalid units. Please specify Celsius or Fahrenheit.")

        elif "define" in query:
            word_to_define = query.replace("define", "").strip()
            search_wikipedia(f"Definition of {word_to_define}")

        elif "set alarm" in query:
            speak("Sir please tell me the time to set alarm.")
            tt = take_command()
            tt = tt.replace("set alarm to ","")
            tt = tt.replace(".","")
            tt = tt.upper()
            MyAlarm.alarm(tt)

        elif "set countdown" in query:
            try:
                speak("Please enter countdown duration in seconds: ")
                duration = int(input("Enter countdown duration in seconds: "))
                if duration > 0:
                    speak(f"Countdown set for {duration} seconds.")
                    countdown_timer(duration)
                else:
                    speak("Invalid duration. Please enter a positive number.")
            except ValueError:
                speak("Invalid input. Please enter a valid number.")

        elif "close this application" in query:
            close_current_application()

        elif "switch the window" in query:
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            pyautogui.keyUp('alt')

        elif "minimise all window" in query:
            pyautogui.keyDown('win')
            pyautogui.press('d')
            pyautogui.keyUp('win')

        elif 'minimise this window' in query or 'minimize current window' in query or 'minimize this' in query or 'minimise current window' in query:
           pyautogui.keyDown("win")
           pyautogui.press("down")
           pyautogui.keyUp("win")
           speak("Current window has been minimized")

        elif "call" in query:
            make_phone_call()

        elif "volume up" in query:
            pyautogui.press("volumeup",5)

        elif "volume down" in query:
            pyautogui.press("volumedown",5)

        elif "mute" in query:
            pyautogui.press("volumemute")

        elif "lock screen" in query:
            ctypes.windll.user32.LockWorkStation()

        elif "check phone number" in query or "check mobile number" in query:
            speak("Sure sir! Can you provide me the country code.")
            country_code = int(input())
            speak("Sir can you provide me the number.")
            number = int(input())
            check_phonenumber(number,country_code)

        elif "horoscope" in query:
            speak("Sure sir!")
            sign = "Aries"
            get_horoscope(sign)

        elif "change window theme" in query or "change system theme" in query:
            speak("Sure sir! Do you want to change it into dark or light mode?")
            mode = take_command().lower()
            if "dark" in mode:
                change_theme("AppsUseLightTheme",0)
            elif "light" in mode:
                change_theme("AppsUseLightTheme",1)

        elif "open camera" in query:
            open_camera()

        elif "close camera" in query:
            cv2.destroyAllWindows()
            speak("Closing the camera.")

        elif "take screenshot" in query:
            screenshot_name = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            pyautogui.screenshot(screenshot_name)
            speak(f"Screenshot taken and saved as {screenshot_name}.")

        elif "bluetooth on" in query:
            subprocess.run("bthprops.cpl", shell=True)
            speak("Bluetooth is now turned on.")

        elif "stop" in query or "exit" in query or "cancel" in query:
            speak("Okay! If you need anything, I'll be here. Have a great day!")
            break

        elif "goodbye" in query or "bye" in query:
            speak("Goodbye! If you need any assistance, don't hesitate to call me.")

        else:
            speak("I'm here to assist you. If you have any specific commands or questions, feel free to ask.")

if __name__ == "__main__":
    load_user_preferences()
    try:
        while True:
            permission = take_command().lower()
            if "wake up" in permission:
                execute_query()
            elif "stop" in permission or "exit" in permission or "cancel" in permission:
                speak("Exiting Jarvis. Have a great day!")
                break
            else:
                execute_query(permission)

    except KeyboardInterrupt:
        print(f"Program terminated by {user_preferences['name']}.")
        save_user_preferences()