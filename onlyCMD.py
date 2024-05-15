import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pywhatkit as kit
import geocoder
from geopy.geocoders import Nominatim
import subprocess
import cv2
import pyautogui
import pyjokes
from Jarvis.features.gui import Ui_MainWindow

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voices', voices[1].id)
engine.setProperty('rate',150)
engine.setProperty('pitch',50)

# Text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# To convert voice into text
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening....")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
    except Exception as e:
        speak("Say that again, please....")
        return "none"
    return query

# To wish
def wish():
    hour = int(datetime.datetime.now().hour)

    speak("Initializing Jarvis")
    speak("Starting all systems applications")
    speak("Installing and checking all drivers")
    speak("Caliberating and examining all the core processors")
    speak("Checking the internet connection")
    speak("Wait a moment sir")
    speak("All drivers are up and running")
    speak("All systems have been activated")
    speak("Now I am online")

    if 0 <= hour < 12:
        print("good morning boss")
        speak("Good morning")
    elif 12 <= hour < 17:
        print("Good Afternoon Boss")
        speak("Good afternoon")
    elif hour>=17 and hour<21:
        print("Good Evening Boss")
        speak("Good Evening Boss")
    else:
        print("good night boss")
        speak("Good night boss")
    speak("I am Jarvis, sir. Please tell me how can I help you")

# Function to get user's location 
def get_location():
      g = geocoder.ip('me')
      location = g.latlng
      return location
def get_location():
    try:
        # Use IP-based location first
        g = geocoder.ip('me')
        location = g.latlng

        # If IP-based location is not available, try GPS-based location
        if not location:
            speak("GPS-based location not available. Please make sure your device has GPS enabled.")
            return None

        return location
    except Exception as e:
        print(f"Error getting location: {e}")
        return None

#get place method

def get_place_name(latitude, longitude):
    try:
        geolocator = Nominatim(user_agent="geo_locator")
        location = geolocator.reverse((latitude, longitude), language='en')
        return location.address
    except Exception as e:
        print(f"Error getting place name: {e}")
        return None
 
#notepad code
def open_notepad():
    speak("Opening Notepad. What do you want to write?")
    text_to_write = takeCommand().lower()

    if text_to_write != "none":
        with open("user_input.txt", "w") as file:
            file.write(text_to_write)

        subprocess.Popen(["notepad.exe", "user_input.txt"]) 
def open_camera():
    cap = cv2.VideoCapture(0)

    while True:
        ret, img = cap.read()
        cv2.imshow('webcam', img)
        
        # Break the loop if the 'Esc' key is pressed
        if cv2.waitKey(50) == 27:
            break

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

    


if __name__ == "__main__":
    wish()
    while True:
        query = takeCommand().lower()
    

        # Logic building for tasks
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            try:  

               query = query.replace("wikipedia", "")
               results = wikipedia.summary(query, sentences=2)
               speak("According to Wikipedia")
               print(results)
               speak(results)
            except:
                speak("No Resultd found...")
                print("No Resultd found...")
        elif 'play ' in query:
            query=query.replace('play' , '') 
            speak('playing' + query) 
            kit.playonyt(query)    

        elif 'open notepad' in query:
            open_notepad()
        elif"open camera" in query:
            open_camera()
        elif  "close camera" in query:
              cv2.destroyAllWindows()   

        elif 'open youtube' in query:
            speak("Sir , What do you want to search on youtube")
            search_query = takeCommand().lower()
            webbrowser.open("https://www.youtube.com/results?search_query="+search_query)

        elif ' time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak( f"Sir, the time is {strTime}")

        elif 'send message' in query:
    # Add logic for sending a message
       
          speak("Sir, tell a message")
          search_query = takeCommand().lower()
          webbrowser.open("https://wa.me/+918779908548?text="+search_query)
  
        elif 'google chrome' in query:
            speak("Sir, what should I search on Google?")
            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
            while True:
                chromeQuery=takeCommand().lower()
                if "search" in chromeQuery:
                    youtubeQuery= chromeQuery
                    youtubeQuery=youtubeQuery.replace("search","")
                    pyautogui.write(youtubeQuery)
                    pyautogui.press('enter')
                    speak('searching....')
                elif "close chrome"in chromeQuery or "exit chrome" in chromeQuery: 
                    pyautogui.hotkey('ctrl' ,'w')
                    speak("Closing Google Chrome sir...")
                    break
           # search_query = takeCommand().lower()
           # webbrowser.open("https://www.google.com/search?q="+search_query)
        elif 'jarvis' in query:
            speak("Hukoom ,  Merey , aaqa")

        elif 'my location' in query:
            location = get_location()
            # speak(f"Sir, your current location is latitude {location[0]} and longitude {location[1]}")
            place_name = get_place_name(location[0], location[1])
            speak(f"Sir, you are currently at {place_name}")

        elif "shutdown" in query: 
            speak ("shutting down")
            os.system('C:\\Windows\\System32\\shutdown.exe /s /t 0')
        elif 'type' in query :
           #  query=query.replace('type', '')
             speak("please tell me what should i write")
             while True:
                writeInNotepad=takeCommand()
                if writeInNotepad=='exit typing':
                    speak("Done Sir")
                else:
                    pyautogui.write(writeInNotepad)
        elif 'joke' in query:
            joke=pyjokes.get_joke()
            print(joke)
            speak(joke)
         
        elif "open camera" in query:
            cap = cv2.VideoCapture(0) 
            while True:
               ret,img = cap.read()
               cv2.imshow('webcam', img) 
               k = cv2.waitKey(50)
               if k==27:
                break
            cap.release()
            cv2.destroyAllwindows() 
            

        elif 'exit' in query or 'quit' in query or 'chup' in query:
            speak("Goodbye, boss!")
            break
