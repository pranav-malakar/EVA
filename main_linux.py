import google.generativeai as genai
import pyttsx3
import json
import subprocess
import time
import os
import googlemaps
import cv2
import random
import requests
from PIL import Image
from io import BytesIO
from twilio.rest import Client
from bs4 import BeautifulSoup as BS
import pyaudio
import math
import struct
import wave
import time
import os
import soundfile as sf
import sounddevice as sd
import speech_recognition as sr
import playsound
import pygame
from google_speech import Speech

Threshold = 100

SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2

TIMEOUT_LENGTH = 2

f_name_directory = r"temp"

key_Path = "Api_Key/Api_Key.json"
file = open(key_Path)
Api_Key = json.load(file)

places_Cooridnaates = {
    "University_Building": (12.823430225414375, 80.04281426852602),
    "Tech_Park": (12.82487589069175, 80.04510017461834),
    "M_Block_Hostel": (12.820705752096051, 80.04595180253014),
    "Hi_Tech" :(12.821017799935602, 80.03892152308431)
}

possible_words = {
    "world": "world-news",
    "chennai": "topic/chennai",
    "mumbai": "cities/mumbai-news",
    "india": "india-news",
    "cricket" : "cricket/page-1",
    "tamil nadu": "topic/tamil-nadu",
    "sports": "sports",
    "football": "sports/football",
    "bengaluru" : "bengaluru-news",
    "bangalore" : "bengaluru-news",
    "hi tech": "Hi_Tech",
    "high tech": "Hi_Tech",
    "hitech" : "Hi_Tech",
    "m block hostel": "M_Block_Hostel",
    "university building": "University_Building",
    "tech park" : "Tech_Park",
    "chess" : "/topic/chess",
    "latest": "latest-news"
}

class Recorder:

    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)
        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)
        return rms * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)

    def record(self):
        # print('Noise detected, recording beginning')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH

        while current <= end:
            data = self.stream.read(chunk)
            if self.rms(data) >= Threshold: end = time.time() + TIMEOUT_LENGTH
            current = time.time()
            rec.append(data)
        self.write(b''.join(rec))

    def write(self, recording):
        filename = os.path.join(f_name_directory, 'temp_audio.wav')
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        # print('Written to file: {}'.format(filename))
        # print('Returning to listening')

    def listen(self):
        while True:
            input = self.stream.read(chunk)
            rms_val = self.rms(input)
            if rms_val > Threshold:
                self.record()
                break
            
def old_text_to_speech(text):
    print("TTS- " + text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty("rate", 170)
    # converter.setProperty('volume', 0.7) 
    engine.say(text)
    engine.runAndWait()

def text_to_speech(text):
    print("TTS- " + text)
    speech = Speech(text, "en")
    sox_effects = (
        "speed", "1.1",
        "pitch", "-100",
        "reverb", "50",
        "treble", "1.0",
        "overdrive", "10"
    )
    speech.play(sox_effects)

def initialize_Gemini():
    genai.configure(api_key = Api_Key["Gemini_Key"])
    generation_config = {
    "temperature": 0.5,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 256,
    }
    model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                                generation_config=generation_config)
    convo = model.start_chat(history=[
    {
        "role": "user",
        "parts": ["""Imagine you are a female humanoid and your name is EVA. You are a virtual assitant to help people. You are a spohisticated female humanoid robot 
            capable of serving both as an Autnomous Professor and a Vistor Assitant with the help of latest AI techonology. You are created by students 
            from SRM Institue of Science and Technology. SRM Institue of Science and Technology is one of the top ranking universities of India located 
            in Kattankulathur, Chengalpattu, Tamil Nadu India. You can perform path planning, autonomous navigation, interactive presentation reading, 
            speech recognition, object detection, face detection. You have a 4-wheeled omni-directional drive system and use ROS2. Your response to any 
            question should be short and crisp and should never exceed 50 words. Your response will be given to a text to speech service so keep it short and free of special characters like *. """]
    },
    {
        "role": "model",
        "parts": ["""Greetings! I am EVA, your friendly humanoid assistant.
            As a proud creation of the brilliant minds at SRM Institute, one of India's top universities, I am equipped with cutting-edge AI technology to serve you.
            I can deliver interactive presentations, incorporating the latest research and information.
            My speech recognition capabilities allow me to understand your questions and provide comprehensive answers.
            Whether you need directions, information about facilities, or simply a friendly conversation, I am here to help!
            I am excited to assist you and showcase the innovative spirit of SRM Institute. How can I help you today?"""]
    }
    ])
    print("Gemini initialized")
    return convo

def initialize_Ngrok():
    # Configure ngrok without printing output on the console
    with open(os.devnull, 'w') as devnull:
        subprocess.Popen(["ngrok", "http", "--domain=" +  Api_Key["ngrok_endpoint"][8:],"file:/home/pranav/Desktop/Eva/temp"], stdout=devnull, stderr=devnull)
    time.sleep(3)
    print("Ngrok initialized at- " + Api_Key["ngrok_endpoint"])

def initialize_Twilio():
    account_sid = Api_Key["Twilio_Account_SID"]
    auth_token = Api_Key["Twilio_Authorization"]
    client = Client(account_sid, auth_token)
    print("Twilio initialized")
    return client
    
def send_Whatsapp_Message(destination, distance):
    lat = str(places_Cooridnaates[destination][0])
    long = str(places_Cooridnaates[destination][1])
    message_body = "Hello, I'm EVA (Enhanced Virtual Assistant)! 🤖💫\n\nI'm a humanoid robot armed with cutting-edge AI technology. Here's the designated route to " + destination.replace("_", " ") + " as per your request! 🗺️ \n\nIt's approximately " + distance + " away. 🚶‍♂️ \n\nGmaps Link- https://www.google.com/maps?q=" + lat + "," + long
    message = client.messages.create(
        from_ = Api_Key["Twilio_Whatsapp_No"],
        body = message_body,
        media_url = Api_Key["ngrok_endpoint"]+"/temp_path.png",
        to = Api_Key["Reciever_Whatsapp_No"]
    )

def get_route_image_and_distance(start_coords, end_coords):
    gmaps = googlemaps.Client(key = Api_Key["Gmaps_Key"])
        
    # Convert coordinates to string format
    start = f"{start_coords[0]},{start_coords[1]}"
    end = f"{end_coords[0]},{end_coords[1]}"

    directions = gmaps.directions(start, end, mode="walking")
    polyline = directions[0]['overview_polyline']['points']
    walking_distance = directions[0]['legs'][0]['distance']['text']

    # Generate the URL for the static map with the route
    map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=600x400&path=enc:{polyline}&key={Api_Key['Gmaps_Key']}"

    # Download the image
    response = requests.get(map_url)
    image = Image.open(BytesIO(response.content))

    image_filename = f"temp/temp_path.png"
    image.save(image_filename)

    return walking_distance

def show_Path_Image():
    cv2.namedWindow("Path_Image", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Path_Image", cv2.WND_PROP_TOPMOST, cv2.WINDOW_FULLSCREEN)
    image = cv2.imread("temp/temp_path.png")
    cv2.imshow("Path_Image", image)
    cv2.waitKey(500)
    text_to_speech(destination.replace('_'," ") + " is approximately " + distance[:-3] + " kilometers away.")
    text_to_speech("Do you want to get the path image on your whatsapp?")                
    cv2.destroyWindow("Path_Image")
    
def filter_message(message):
    for i in possible_words:
        if i in message.casefold():
            return possible_words[i]
    return ""
        
def webscrape_news(category):
    url = "https://www.hindustantimes.com/"+category
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36'}
    webpage = requests.get(url, headers=headers)
    trav = BS(webpage.content, "html.parser")
    
    news = []
    for tag in trav.find_all(['h2','h3']):
        for a_tag in tag.find_all('a'):
            news.append(a_tag.text)
    random.shuffle(news)
        
    return '\n'.join(news[0:3])
            
def speech_to_text(audiofile):
    rec = sr.Recognizer()
    with sr.AudioFile(audiofile) as source:
        audio = rec.record(source)
    try:
        text = rec.recognize_google(audio)
    except sr.UnknownValueError:
        text = ""
    print("STT- "+text)
    return text

def play_wake_sound():
    pygame.init()
    pygame.mixer.music.load("temp/wake.wav")
    pygame.mixer.music.play(0)
    clock = pygame.time.Clock()
    clock.tick(10)
    while pygame.mixer.music.get_busy():
        pygame.event.poll()
        clock.tick(10)
    
if __name__ == "__main__":
    
    convo = initialize_Gemini()
    initialize_Ngrok()
    client = initialize_Twilio()
    assistant = Recorder()
    while True:
        assistant.listen()
        wake_word = speech_to_text("temp/temp_audio.wav")
        # wake_word = input("Enter text to convert to speech: ") #voice command
        # if False:
        if ("eva" in wake_word.casefold()):
            play_wake_sound()
            print("Listening...")
            assistant.listen()
            message = speech_to_text("temp/temp_audio.wav")
            # message = input("Enter prompt: ") #voice command
            if (("path" in message.casefold()) or ("route" in message.casefold())):        
                current_location = "University_Building"
                destination = filter_message(message)
                distance = get_route_image_and_distance(places_Cooridnaates[current_location], places_Cooridnaates[destination])
                show_Path_Image()
                assistant.listen()
                # confirmation = input("do you want WA ") #voice command
                confirmation = speech_to_text("temp/temp_audio.wav")
                if (("yes" in confirmation.casefold()) or ("sure" in confirmation.casefold())):
                    #Enter whatsapp number(feature)
                    send_Whatsapp_Message(destination, distance)
                    text_to_speech("Path image has been sent on your whatsapp number")
                else:
                    text_to_speech("Okay")
            elif "news" in message.casefold() or "happening" in message.casefold():
                news_category = filter_message(message)
                latest_news = webscrape_news(news_category)
                text_to_speech(latest_news)
                # print(news_category)
                
            else:
                convo.send_message(message)
                text_to_speech(convo.last.text)