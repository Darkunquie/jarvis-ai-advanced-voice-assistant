import pyttsx3
import datetime
import speech_recognition as sr
import smtplib
from secrets import senderemail,epwd,to
from email.message import EmailMessage
import pyautogui
import webbrowser as wb
from time import sleep
import wikipedia  # Ensure you use this module somewhere in your code
import pywhatkit
import requests
import geocoder 
from newsapi import NewsApiClient
import pyperclip as clipboard
import os
import subprocess
import time 
import threading
import string
import random
import logging
#from nltk.tokenize import word_tokenize

engine =pyttsx3.init()
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
logging.basicConfig(level=logging.INFO)

def getvoices(voice):
    voices= engine.getProperty('voices')
    #printf(voices[0].id)
    if voice==1:
        engine.setProperty('voice',voices[0].id)
        speak("hello, this is jarvis")     
    if voice==2:
         engine.setProperty('voice',voices[1].id)
         speak("hello, this is friday")     

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("the current time is:")
    speak(Time)    
def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak("the current date is:")
    speak(date)
    speak(month)
    speak(year)
def greeting():
    hour=datetime.datetime.now().hour
    if hour>=6 and hour <12 :
        speak("good morning sir!")
    elif hour >=12 and hour <18:
        speak("goof afternoon sir!")
    elif hour>=18 and hour<24 :
        speak("Good evening sir!")
    else:
        speak("good night sir!")              
def wishme():
    speak("welcome back sir!")
    time()
   # date()
    greeting()
    speak("jarvis at your service ,please tell me how can i help you?")
# while True:
   # voice = int(input("press 1 for male voice\npress 2 for female voice\n"))
   #2 speak(audio)

   # getvoices(voice)
#wishme()
#time()
#date()
def takeCommandCMD():
    query =input("please tell me how can i help you\n")
    return query
def takeCommandMic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...........")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...........")
        query = r.recognize_google(audio, language='en-IN')
        print(f"Recognized command: {query}")  # Debug print to see the recognized command
        
        # Check if the user wants to set a reminder
        if 'remind me to' in query:
            task = query.split('remind me to')[1].strip()  # Extract the task
            speak("When should I remind you?")
            time_delay = takeCommandMic()  # User specifies the time
            delay = parse_time_delay(time_delay)  # Convert to seconds
            schedule_task(task, delay)  # Schedule the task
            speak(f"I will remind you to {task} in {time_delay}.")
            return "none"  # Return early since we handled the reminder

    except Exception as e:
        print(e)
        speak("Say it again please........")
        print("repeat again...................")
        return "none"
    
    return query
def sendEmail(receiver, subject, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(senderemail, epwd)
        email = EmailMessage()
        email['From'] = senderemail
        email['To'] = " ".join(receiver)
        email['Subject'] = subject
        email.set_content(content)
        server.send_message(email)
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        speak("Unable to send the email.")
def sendwhatsmg(phone_no,message):
    
    Message = message
    wb.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+Message)
    sleep(10)
    pyautogui.press('enter')
def searchgoogle():
    speak("what should i search on google?")
    search=takeCommandMic()
    url=f"https://www.google.com/search?q={search}"
    wb.open(url)
    speak(f"searching {search} on google")
def news():
    stop_event = threading.Event()  # Create an event to signal stopping

    def listen_for_stop():
        recognizer = sr.Recognizer()  # Initialize the recognizer
        with sr.Microphone() as source:
            while not stop_event.is_set():  # Listen until the stop event is set
                try:
                    audio = recognizer.listen(source)  # Listen for audio
                    command = recognizer.recognize_google(audio)  # Recognize speech
                    if "stop" in command.lower():  # Check if the command is to stop
                        stop_event.set()  # Set the stop event
                except sr.UnknownValueError:
                    continue  # Ignore unrecognized speech
                except sr.RequestError:
                    print("Could not request results from Google Speech Recognition service")
                    break

    def speak_news():
        newsapi = NewsApiClient(api_key='11c10c3f1df54d0d97921ac7b87df3a2')
        top = newsapi.get_top_headlines(sources='bbc-news', language='en', page_size=2,q='latest')
        speak("here are some headlines")
        newsdata=top['articles']
        for i in newsdata:
            speak(i['title'])
            print(i['title'])
            speak(i['description'])
            print(i['description'])
        speak("thats all the news for today")

    # Start the listening thread
def text2speech():
    text=clipboard.paste()
    print(text)
    speak(text)
def screenshot():
    name_img = datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S") 
    #name_img = f'D:\\projects\\screenshot\\screenshot_{name_img}.png'  # Correctly format the file path
    img = pyautogui.screenshot()
    img.show()
    img.save(name_img)
def passwordgen():
    s1 = string.ascii_uppercase
    s2 = string.ascii_lowercase
    s3 = string.digits
    s4 = string.punctuation

    # Ask for password length with a minimum requirement
    while True:
        speak("Please tell me the password length. It should be at least 8 characters.")
        passlen = takeCommandMic()
        if passlen.lower() == "none":
            speak("I didn't catch that. Please tell me the password length again.")
            continue
        try:
            passlen = int(passlen)
            if passlen < 8:  # Minimum length check
                speak("The password length should be at least 8 characters. Please try again.")
                continue
            break
        except ValueError:
            speak("That doesn't seem to be a valid number. Please tell me the password length again.")

    # Ask for complexity options
    speak("Do you want to include uppercase letters, lowercase letters, digits, and special characters? Please say yes or no for each.")
    include_upper = takeCommandMic().lower() == "yes"
    include_lower = takeCommandMic().lower() == "yes"
    include_digits = takeCommandMic().lower() == "yes"
    include_special = takeCommandMic().lower() == "yes"

    # Build the character set based on user preferences
    s = []
    if include_upper:
        s.extend(list(s1))
    if include_lower:
        s.extend(list(s2))
    if include_digits:
        s.extend(list(s3))
    if include_special:
        s.extend(list(s4))

    if not s:
        speak("You must include at least one type of character. Please try again.")
        return

    random.shuffle(s)
    password = "".join(s[:passlen])
    print(password)
    speak(f"Your generated password is: {password}")

    # Provide feedback on password strength
    strength = "weak"
    if passlen >= 12 and (include_upper and include_lower and include_digits and include_special):
        strength = "strong"
    elif passlen >= 10:
        strength = "medium"
    
    speak(f"This password is considered {strength}.")
def schedule_task(task, delay):
    def task_function():
        speak(f"Time to {task}!")
    timer = threading.Timer(delay, task_function)
    timer.start()    
def parse_time_delay(time_delay):
    # Simple parsing logic to convert time delay to seconds
    if 'minute' in time_delay:
        minutes = int(time_delay.split()[0])
        return minutes * 60  # Convert minutes to seconds
    elif 'hour' in time_delay:
        hours = int(time_delay.split()[0])
        return hours * 3600  # Convert hours to seconds
    elif 'second' in time_delay:
        seconds = int(time_delay.split()[0])
        return seconds  # Already in seconds
    return 0  
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={os.getenv('WEATHER_API_KEY')}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data
    except requests.RequestException as e:
        logging.error(f"Weather request failed: {e}")
        speak("Sorry, I couldn't fetch the weather information.")
    
#xcndEmail()    
#http://api.openweathermap.org/data/2.5/weather?q={hyderabad}&units=metric&appid={e707c56931ce54b4f57ca706ef449162}
if __name__ == "__main__":
    getvoices(1)
    #wishme()
    #listen_for_stop()   
    while True:
        query =takeCommandMic().lower()
        #query=word_tokenize(query)
        print(query)
        print()
        if 'time' in query:
            time()
        elif 'date' in query:
            date()    

        elif 'email' in query:
            email_list={
                'test email':'darkunquie1@gmail.com'
            }
            try:
                speak("to whom you want to send the email")
                name=takeCommandMic()
                receiver=email_list[name]
                speak("what is the subject of the mail?")
                subject = takeCommandMic()
                speak("what should i say?")
                content = takeCommandMic()
                sendEmail(receiver,subject,content)
                speak("your email has been sent!")
            except Exception as e:
                print(e)
                speak("unable to end the email")  
        elif 'message' in query:
            user_name  ={
                'Aruna':'+91 9959562946',
                'keer' :'+91 8919198607'
            }
            try:
                speak("to whom you want to send the whats app message?")
                name=takeCommandMic()
                phone_no=user_name[name]
                speak("what is the message?")
                message = takeCommandMic()
                sendwhatsmg(phone_no,message)
                speak("message has been sent!")
            except Exception as e:
                print(e)
                speak("unable to send the message")  
                
        elif  'youtube' in query:
            speak("what should i search on youtube?")
            search=takeCommandMic()
            pywhatkit.playonyt(search)
            speak("youtube video has been opened")

        elif 'weather' in query:
            speak("please tell me the city name.")
            city = takeCommandMic()
            
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=e707c56931ce54b4f57ca706ef449162"
            response = requests.get(url)
            data = response.json()
                
            if response.status_code == 200:  # Check if the request was successful
                weather = data['weather'][0]['main']
                temperature = data['main']['temp']
                desp = data['weather'][0]['description']
                temperature = round(temperature)  # No need for conversion, API returns in Celsius
                    
                speak(f"the weather in {city} is {weather} and the temperature is {temperature} degree Celsius")
                print(desp)
                speak(desp)
                print(weather)
                speak(weather)
                print(temperature)
                speak(f"Temperature: {temperature} degree Celsius")
                speak(f'Weather is {desp}')
            else:
                speak(f"Sorry, I couldn't find the weather for {city}.")
                    
        elif 'current location weather' in query or 'current weather' in query:
            # Get the user's current location
            g = geocoder.ip('me')
            latitude = g.latlng[0]
            longitude = g.latlng[1]
            
            # Fetch weather data using latitude and longitude
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid=e707c56931ce54b4f57ca706ef449162"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:  # Check if the request was successful
                weather = data['weather'][0]['main']
                temperature = data['main']['temp']
                desp = data['weather'][0]['description']
                temperature = round(temperature)  # No need for conversion, API returns in Celsius
                
                speak(f"The current weather is {weather} and the temperature is {temperature} degree Celsius.")
                print(desp)
                speak(desp)
                print(weather)
                speak(weather)
                print(temperature)
                speak(f"Temperature: {temperature} degree Celsius")
                speak(f'Weather is {desp}')
            else:
                speak("Sorry, I couldn't find the weather for your current location.")
        elif 'news' in query:
            news()
        elif 'google' in query:
            searchgoogle()
        elif 'read' in query:
            text2speech()
        
        elif 'notepad' in query: 
            os.system('start notepad')
            speak("notepad has been opened")
        
                
        elif  'open google' in query:
            try:
                subprocess.run(['start', 'chrome', 'https://www.google.com'], shell=True)  # Open Google homepage in Chrome
                speak("Google has been opened")
            except Exception as e:
                print(e)
                speak("I couldn't open Google.")
        
        elif 'open whatsapp' in query:
            os.system('start chrome')  # Assuming WhatsApp Web is opened in Chrome
            speak("whatsapp has been opened")
        elif 'close whatsapp' in query:  # Added condition to close WhatsApp
            try:
                os.system('taskkill /f /im chrome.exe')  # Close Chrome if WhatsApp Web is open
                speak("whatsapp has been closed")
            except Exception as e:
                print(e)
                speak("I couldn't close whatsapp.")
                
        elif ' cmd' in query:
            os.system('start cmd')
            speak("cmd has been opened")
        elif 'close cmd' in query:  # Added condition to close Command Prompt
            try:
                os.system('taskkill /f /im cmd.exe')  # Forcefully close Command Prompt
                speak("cmd has been closed")
            except Exception as e:
                print(e)
                speak("I couldn't close cmd.")
        elif  'open ms word' in query:
            os.system('start winword')
            speak("ms word has been opened")
        elif 'close ms word' in query:  # Added condition to close MS Word
            try:
                os.system('taskkill /f /im winword.exe')  # Forcefully close MS Word
                speak("ms word has been closed")
            except Exception as e:
                print(e)
                speak("I couldn't close ms word.")
        elif 'open settings' in query:
            speak("What should I search in settings?")
            search_query = takeCommandMic()  # Get the search query from the user
            os.system(f'start ms-settings:search?search={search_query}')  # Open Windows Settings with search
            sleep(5)  # Wait for a few seconds to allow the user to see the settings
            os.system('taskkill /f /im Settings.exe')  # Close the Settings app
            speak("Settings has been closed")

        elif 'doc' in query:
            index = query.index('doc')  # Find the index of 'open'
            folder_name = ' '.join(query[index + 1:])  # Get everything after 'open'
            
            # Define common folder paths
            common_folders = {
                "documents": "C:\\Users\\YASHU\\OneDrive\\Documents",
                "downloads": "C:\\Users\\YASHU\\Downloads",
                "pictures": "C:\\Users\\YASHU\\OneDrive\\Pictures",
                "music": "C:\\Users\\YASHU\\OneDrive\\Music",
                "desktop": "C:\\Users\\YASHU\\OneDrive\\Desktop"
            }
            
            # Get the folder path from the dictionary
            folder_path = common_folders.get(folder_name.lower())
            
            if folder_path and os.path.exists(folder_path) and os.path.isdir(folder_path):
                os.system('explorer "{}"'.format(folder_path))
                speak("Folder has been opened")
            else:
                speak("Sorry, I couldn't find that folder.")  # Get user input for the file name
                
           
        elif 'screenshot' in query:
            screenshot()
            speak("screenshot has been taken")
            speak("do you want to save it?")
            save = takeCommandMic()
            if 'yes' in save:
                speak("where should I save it?")
                path = takeCommandMic()
                path = path.replace('save in', '')
                path = path.replace('save it in', '')
                img = pyautogui.screenshot()
                # Save the screenshot to the specified path
                img.save(path)  # Save the screenshot to the user-defined path
                speak("screenshot has been saved")
                speak("screenshot task is accomplished")
            elif 'no' in save:  # Added condition to handle 'no' response
                speak("screenshot will not be saved.")
                speak("screenshot task is accomplished")
        elif 'remember this' in query:
            speak("what should i remember?")
            data=takeCommandMic()
            speak("you said me to remember that "+data)
            remember=open('data.txt','w')
            remember.write(data)
            remember.close()
            speak("i will remember that")
            speak("remembering task is accomplished")   
        elif 'what did i ask you to remember' in query:
            remember= open('data.txt', 'r')
            speak("you asked me to remember that " + remember.read())
            remember.close()
        elif 'password' in query:
            passwordgen()
            speak("password generation task is accomplished")
        
        
        elif 'offline' in query:
             speak("thank you sir!")
             quit()
#takeCommandMic==" hey jarvis"
