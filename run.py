from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QMovie
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import pyttsx3
import speech_recognition as sr
import os
import time
import webbrowser
import datetime
import wikipedia
import geocoder
from geopy.geocoders import Nominatim
import subprocess
import cv2
import pyautogui
import pyjokes
import pywhatkit as kit
from bs4 import BeautifulSoup
import requests
import speedtest
from time import sleep
from pynput.keyboard import Key, Controller
from plyer import notification


flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voices", voices[1].id)
engine.setProperty("rate", 150)
engine.setProperty("pitch", 50)
keyboard = Controller()


def volumeup():
    for i in range(5):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        sleep(0.1)


def volumedown():
    for i in range(5):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        sleep(0.1)


# Define a class to hold signals
class SignalHolder(QObject):
    output_changed = pyqtSignal(str)


signal_holder = SignalHolder()


def setOutput(text):
    output = text
    signal_holder.output_changed.emit(output)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    setOutput(audio)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening....")
        setOutput("listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        setOutput("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"user said: {query}")
        setOutput("user said : " + query)
    except Exception as e:
        speak("Say that again, please....")
        return "none"
    return query


def wish():
    hour = int(datetime.datetime.now().hour)

    speak("Initializing")
    speak("Starting all systems applications")
    speak("Installing and checking all drivers")
    speak("Checking the internet connection")
    speak("Wait a moment sir")
    speak("All drivers are up and running")
    speak("All systems have been activated")
    speak("Now I am online")

    if 0 <= hour < 12:
        print("Good morning Sir")
        speak("Good morning Sir")
    elif 12 <= hour < 17:
        print("Good Afternoon Sir")
        speak("Good afternoon Sir")
    elif hour >= 17 and hour < 21:
        print("Good Evening Sir")
        speak("Good Evening Sir")
    else:
        print("good night Sir")
        speak("Good night Sir")
    speak("I am Jarvis, sir. Please tell me how can I help you")


# Function to get user's location
def get_location():
    g = geocoder.ip("me")
    location = g.latlng
    return location


def get_location():
    try:
        # Use IP-based location first
        g = geocoder.ip("me")
        location = g.latlng

        # If IP-based location is not available, try GPS-based location
        if not location:
            speak(
                "GPS-based location not available. Please make sure your device has GPS enabled."
            )
            return None

        return location
    except Exception as e:
        print(f"Error getting location: {e}")
        speak("Location not found")
        return None


# get place method


def get_place_name(latitude, longitude):
    try:
        geolocator = Nominatim(user_agent="geo_locator")
        location = geolocator.reverse((latitude, longitude), language="en")
        return location.address
    except Exception as e:
        print(f"Error getting place name: {e}")
        speak("Place name not found")
        return None


# notepad code
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
        cv2.imshow("webcam", img)
        # Break the loop if the 'Esc' key is pressed
        if cv2.waitKey(50) == 27:
            break

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()


class mainT(QThread):
    def __init__(self):
        super(mainT, self).__init__()
        self.conversation_active = False  # Flag to control conversation

    def run(self):
        if self.conversation_active:
            self.start_conversation()

    def start_conversation(self):
        wish()
        while self.conversation_active:
            # ls.lsHotword_loop("")
            query = takeCommand().lower()
            if "wikipedia" in query:
                speak("Searching Wikipedia...")
                try:
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                except:
                    speak("No Resultd found...")
                    print("No Resultd found...")

            elif "play " in query:
                query = query.replace("play", "")
                speak("playing" + query)
                kit.playonyt(query)

            elif "open notepad" in query:
                open_notepad()
            # elif"open camera" in query:
            #     open_camera()
            # elif  "close camera" in query:
            #     cv2.destroyAllWindows()
            elif "click my photo" in query:
                pyautogui.press("super")
                pyautogui.typewrite("camera")
                pyautogui.press("enter")
                pyautogui.sleep(2)
                speak("SMILE")
                pyautogui.press("enter")

            elif "temperature" in query:
                search = "temperature in mumbai"
                url = f"https://www.google.com/search?q={search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text, "html.parser")
                temp = data.find("div", class_="BNeawe").text
                speak(f"current{search} is {temp}")

            elif "open youtube" in query:
                speak("Sir , What do you want to search on youtube")
                search_query = takeCommand().lower()
                webbrowser.open(
                    "https://www.youtube.com/results?search_query=" + search_query
                )

            elif "search" in query:  # EASY METHOD
                query = query.replace("search", "")
                query = query.replace("jarvis", "")
                pyautogui.press("super")
                pyautogui.typewrite(query)
                pyautogui.sleep(2)
                pyautogui.press("enter")

            elif "time" in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                print(strTime)
                speak(f"Sir, the time is {strTime}")

            elif "send message" in query:
                # Add logic for sending a message

                speak("Sir, tell a message")
                search_query = takeCommand().lower()
                webbrowser.open("https://wa.me/+918779908548?text=" + search_query)

            elif "chrome" in query:
                speak("Sir, what should I search on Google?")
                os.startfile(
                    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                )
                while True:
                    chromeQuery = takeCommand().lower()
                    if "search" in chromeQuery:
                        youtubeQuery = chromeQuery
                        youtubeQuery = youtubeQuery.replace("search", "")
                        pyautogui.write(youtubeQuery)
                        pyautogui.press("enter")
                        speak("searching....")
                    elif "close chrome" in chromeQuery or "exit chrome" in chromeQuery:
                        pyautogui.hotkey("ctrl", "w")
                        speak("Closing Google Chrome sir...")
                        break
            elif "jarvis" in query:
                speak("Hukoom ,  Merey , aaqa")

            elif "my location" in query:
                location = get_location()
                place_name = get_place_name(location[0], location[1])
                speak(f"Sir, you are currently at {place_name}")
            # calculate mathametical calculations
            elif "calculate" in query:
                # Extract the mathematical expression from the query
                expression = query.replace("calculate", "")
                try:
                    # Evaluate the mathematical expression
                    result = eval(expression)
                    speak(f"The result of {expression} is {result}")
                except Exception as e:
                    speak(
                        "Sorry, I couldn't perform the calculation. Please provide a valid mathematical expression."
                    )
            elif "shutdown" in query:
                speak("Do you wish to shutdown your computer ? say yes or no")
            elif "yes" in query:
                os.system("shutdown /s /t 1")
            elif "type" in query:
                #  query=query.replace('type', '')
                speak("please tell me what should i write")
                while True:
                    writeInNotepad = takeCommand()
                    if writeInNotepad == "exit typing":
                        speak("Done Sir")
                    else:
                        pyautogui.write(writeInNotepad)
            elif "joke" in query:
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)

            elif "hello" in query:
                speak("Hello sir, how are you ?")

            elif "i am fine" in query:
                speak("that's great, sir")

            elif "how are you" in query:
                speak("Perfect, sir")

            elif "thank you" in query:
                speak("you are welcome, sir")

            elif "pause" in query:
                pyautogui.press("k")
                speak("video paused")

            elif "play" in query:
                pyautogui.press("k")
                speak("video played")

            elif "mute" in query:
                pyautogui.press("m")
                speak("video muted")

            elif "volume up" in query:
                from keyboard import volumeup

                speak("Turning volume up,sir")
                volumeup()
            elif "volume down" in query:
                from keyboard import volumedown

                speak("Turning volume down, sir")
                volumedown()
            elif ".com" in query or ".co.in" in query or ".org" in query:
                query = query.replace("open", "")
                query = query.replace("jarvis", "")
                query = query.replace("launch", "")
                query = query.replace(" ", "")
                webbrowser.open(f"https://www.{query}")

            elif "internet speed" in query:
                wifi = speedtest.Speedtest()
                upload_net = wifi.upload() / 1048576  # Megabyte = 1024*1024 Bytes
                download_net = wifi.download() / 1048576
                print("Wifi Upload Speed is", upload_net)
                print("Wifi download speed is ", download_net)
                speak(f"Wifi download speed is {download_net}")
                speak(f"Wifi Upload speed is {upload_net}")

            elif "ipl score" in query:
                url = "https://www.cricbuzz.com/"
                page = requests.get(url)
                soup = BeautifulSoup(page.text, "html.parser")

                # Check if the required elements exist
                team_elements = soup.find_all(class_="cb-ovr-flo cb-hmscg-tm-nm")
                score_elements = soup.find_all(class_="cb-ovr-flo")

                if team_elements and score_elements:
                    team1 = (
                        team_elements[0].get_text()
                        if len(team_elements) > 0
                        else "Team 1"
                    )
                    team2 = (
                        team_elements[1].get_text()
                        if len(team_elements) > 1
                        else "Team 2"
                    )
                    team1_score = (
                        score_elements[8].get_text()
                        if len(score_elements) > 8
                        else "N/A"
                    )
                    team2_score = (
                        score_elements[10].get_text()
                        if len(score_elements) > 10
                        else "N/A"
                    )

                    print(f"{team1} : {team1_score}")
                    print(f"{team2} : {team2_score}")

                    notification.notify(
                        title="IPL SCORE :- ",
                        message=f"{team1} : {team1_score}\n {team2} : {team2_score}",
                        timeout=15,
                    )
                else:
                    print("Error: Required elements not found on the webpage.")

            elif "screenshot" in query:
                screenshot = pyautogui.screenshot()
                screenshot.save("ss.jpg")
                speak("Screenshot taken, sir.")

            elif "exit" in query or "quit" in query or "chup" in query:
                speak("Goodbye, Sir!")
                break


FROM_MAIN, _ = loadUiType(os.path.join(os.path.dirname(__file__), "./gui.ui"))


class Main(QMainWindow, FROM_MAIN):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(1366, 768)

        # background image
        self.label.lower()

        # exit button
        self.exitB.setStyleSheet(
            "background-image:url(./lib/exit - Copy.png);\n" "border:none;"
        )
        self.exitB.clicked.connect(self.close)
        self.exitB.setCursor(Qt.PointingHandCursor)

        # run button
        self.startB.setStyleSheet(
            "background-image:url(./lib/start.png);\n" "border:none;"
        )
        self.startB.setCursor(Qt.PointingHandCursor)
        self.startB.clicked.connect(self.start_conversation_button)
        self.startB.setGeometry(
            QtCore.QRect(1120, 50, 230, 103)
        )  # Adjust position and size as needed

        # gif loader image
        self.setWindowFlags(flags)
        self.Dspeak = mainT()
        self.label_4_movie = QMovie("./lib/gifloader.gif")
        self.label_4.setMovie(self.label_4_movie)
        self.label_4_movie.start()
        self.label_4

        # date and time
        self.ts = time.strftime("%A, %d %B")  # date
        self.ts2 = time.strftime("%H:%M:%S")  # time

        # date
        self.label_5.setText("<font size=8 color='white'>" + self.ts + "</font>")
        self.label_5.setFont(QFont("Acens", 8))
        # self.label_5.move(40, -220)

        # time
        self.label_6 = QLabel(self)
        self.label_6.setGeometry(
            40, 278, 300, 50
        )  # Adjust position and size of self.label_5
        self.label_6.setText(
            "<font size=8 color='white'>" + "Time : " + self.ts2 + "</font>"
        )
        self.label_6.setFont(QFont("Acens", 8))

        # location
        self.localtion_label = QLabel(self)
        self.localtion_label.setGeometry(
            40, 415, 300, 50
        )  # Adjust position and size of self.label_5
        self.localtion_label.setText(
            "<font size=8 color='white'> Location : India </font>"
        )
        self.localtion_label.setFont(QFont("Acens", 8))

        # output label
        signal_holder.output_changed.connect(self.update_output_label)
        self.output_label = QLabel(self)
        self.output_label.setGeometry(
            300, 65, 300, 50
        )  # Adjust position and size of self.label_5
        self.output_label.setText("<font size=7 color='white'></font>")
        self.output_label.setFont(QFont("Acens", 7))
        self.output_label.setAlignment(Qt.AlignCenter)

        # tauheed label
        self.localtion_label = QLabel(self)
        self.localtion_label.setGeometry(
            40, 562, 300, 50
        )  # Adjust position and size of self.label_5
        self.localtion_label.setText(
            "<font size=8 color='white'>  Ansari Tauheed </font>"
        )
        self.localtion_label.setFont(QFont("Acens", 8))

        # Iqbal label
        self.localtion_label = QLabel(self)
        self.localtion_label.setGeometry(
            80, 700, 300, 50
        )  # Adjust position and size of self.label_5
        self.localtion_label.setText(
            "<font size=8 color='white'>  Iqbal Ansari </font>"
        )
        self.localtion_label.setFont(QFont("Acens", 8))

    # update output method
    def update_output_label(self, text):
        self.output_label.setText("<font size=7 color='white'>" + text + "</font>")
        self.output_label.adjustSize()
        label_width = self.output_label.width()
        label_height = self.output_label.height()
        window_width = self.width()  # Get the width of the main window
        x_pos = (
            window_width - label_width
        ) // 2  # Calculate the x position for center alignment
        y_pos = 60  # Set the y position
        self.output_label.setGeometry(x_pos, y_pos, label_width, label_height)

        # time timer
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # 1 second in milliseconds
        self.timer.timeout.connect(self.update_time)  # Connect timer to update function
        self.timer.start()

    def update_time(self):
        self.ts2 = time.strftime("%H:%M:%S")  # Get current time
        self.label_6.setText(
            "<font size=8 color='white'>Time : " + self.ts2 + "</font>"
        )  # Update label text

    def start_conversation_button(self):
        self.Dspeak.conversation_active = True  # Activate conversation in mainT
        self.Dspeak.start()


app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
exit(app.exec_())
