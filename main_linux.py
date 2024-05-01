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
import firebase_admin
from firebase_admin import credentials, db

Threshold = 100

SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2

TIMEOUT_LENGTH = 1

INACTIVE_TIME = 10

f_name_directory = r"temp"

key_Path = "Api_Key/Api_Key.json"
file = open(key_Path)
Api_Key = json.load(file)

places_Cooridnaates = {
    "University_Building": (12.823430225414375, 80.04281426852602),
    "Tech_Park": (12.82487589069175, 80.04510017461834),
    "M_Block_Hostel": (12.820705752096051, 80.04595180253014),
    "Hi_Tech" : (12.821017799935602, 80.03892152308431),
    "SRM_Hotel" :(12.823874739157871, 80.04148745200509),
    "SRM_School_of_Architecture" :(12.82406263228619, 80.04402007264517),
    "SRM_Central_Library" :(12.82352516128309, 80.04241786006341),
    "SRM_Chemical_Block" :(12.824009009357464, 80.04303553004884),
    "Java_Green_Food_Court" :(12.823295588680576, 80.04444680372917),
    "Basic_Engineering_Lab" :(12.823730118888252, 80.04348489168424),
    "Arch_Gate" :(12.823018345550045, 80.04102756383446),
    "Potheri_Station" :(12.821443184988869, 80.03715411731638),
    "TP_Ganesan_Auditorium" :(12.824725978182517, 80.04683662365053),
    "Tech_Park_Ground" :(12.823652433610484, 80.0466311767049),
    "Dental_College" :(12.825220621156651, 80.04745849515895),
    "SRM_Global_Hospital" :(12.82336685837323, 80.04785600738975),
    "SRM_Medical_College" :(12.820719918200233, 80.0481427295616),
    "Biotech Block" :(12.824613998338165, 80.04422202529679),
    "SRM_Arts_and_Science" :(12.82578832477728, 80.04355383038295),
    "CV_Raman_Research_Park" :(12.825044227439289, 80.04441396314071),
    "DEICE" :(12.823480798369017, 80.04359934704149),
    "SRM_University_Admission" :(12.825578929703878, 80.04342252283108),
    "SRM_Valliammai_Engineering_College" :(12.825941985761867, 80.04132033075835),
    "SRM_Mechanical_Block" :(12.820844629008333, 80.03970310563086),
    "Civil_Engineering_Block" :(12.82044409924326, 80.03916291430765),
    "Electrical_Science_Block" :(12.81988445383377, 80.0392979621466),
    "Aerospace_Hanger" :(12.820186223562475, 80.04002384423295),
    "Mechanical_Hanger" :(12.82056480689537, 80.04013075709899),
    "CRC" :(12.820238643788379, 80.03799577739784),
    "Main_Campus_Entrance" :(12.821121092115769, 80.03775594954442),
    "Office" :(12.8200974517599, 80.0385433089774),
    "FAB_LAB" :(12.82238298785626, 80.04573362025894),
    "Boys_Hostel" :(12.822895546316373, 80.04330584296365),
    "SRM_Robocon_Lab" :(12.82380485004579, 80.04335424022312),
    "Shiv_Temple" :(12.821244852349126, 80.04487169093323),
    "SRM_BBA_Block" :(12.825237323647595, 80.04466387053536),
    "SRM_College_of_Agriculture_and_Horiculture" :(12.825334632432396, 80.04539316807005),
    "SRM_Polytechnic_College" :(12.82556418121155, 80.04490441077488),	
    "SRM_College_of_Pharmacy" :(12.82556418121155, 80.04490441077488),
    "Annexure_Campus" :(12.822387485799755, 80.04639081996272)
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
    "chess" : "/topic/chess",
    "latest": "latest-news",
    "bengaluru" : "bengaluru-news",
    "bangalore" : "bengaluru-news",
    "hi tech": "Hi_Tech",
    "high tech": "Hi_Tech",
    "hitech" : "Hi_Tech",
    "hi-tech" : "Hi_Tech",
    "m block hostel": "M_Block_Hostel",
    "university building": "University_Building",
    "tech park" : "Tech_Park",
    "hotel" : "SRM_Hotel",
    "School of Architecture" : "SRM_School_of_Architecture",
    "Library" : "SRM_Central_Library",
    "Chemical Block" : "SRM_Chemical_Block",
    "Java" : "Java_Green_Food_Court",
    "Food Court" : "Java_Green_Food_Court",
    "Basic Engineering Lab" : "Basic_Engineering_Lab",
    "BELL" : "Basic_Engineering_Lab",
    "Arch Gate" : "Arch_Gate",
    "Arch-Gate" : "Arch_Gate",
    "Potheri Staton" : "Potheri_Station",
    "Auditorium" : "TP_Ganesan_Auditorium",
    "Ground" : "Tech_Park_Ground",
    "Dental College" : "Dental_College",
    "Hospital" : "SRM_Global_Hospital",
    "Medical College" : "SRM_Medical_College",
    "Biotech" : "Biotech",
    "Arts and Science" : "SRM_Arts_and_Science",
    "Research Park" : "CV_Raman_Research_Park",
    "Admission" : "SRM_University_Admission",
    "Valliammai" : "SRM_Valliammai_Engineering_College",
    "Valimai" : "SRM_Valliammai_Engineering_College",
    "Aerospace Hangar" : "Aerospace_Hanger",
    "Mechanical Hangar" : "Mechanical_Hanger",
    "Mechanical" : "SRM_Mechanical_Block",
    "Civil" : "Civil_Engineering_Block",
    "Electrical" : "Electrical_Science_Block",
    "CRC" : "CRC",
    "Main Campus" : "Main_Campus_Entrance",
    "FAB Lab" : "FAB_LAB",
    "Boys Hostel" : "Boys_Hostel",
    "Girls Hostel" : "M_Block_Hostel",
    "Robocon" : "SRM_Robocon_Lab",
    "Shiv Temple" : "Shiv_Temple",
    "BBA" : "SRM_BBA_Block",
    "Annexure Campus" : "Annexure_Campus"
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

    def listen(self, timeout):
        now = time.time()
        while True:
            input = self.stream.read(chunk)
            rms_val = self.rms(input)
            if rms_val > Threshold:
                self.record()
                break
            if timeout:
                later = time.time()
                if (int(later - now))>5:
                    play_wake_sound(True)
                    return False
        return True
            
def old_text_to_speech(text):
    text = text.replace("*", "")
    print("TTS- " + text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty("rate", 170)
    # converter.setProperty('volume', 0.7) 
    engine.say(text)
    engine.runAndWait()

def text_to_speech(text):
    text = text.replace("*", "")
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

def initialize_Firebase():
    cred = credentials.Certificate("Api_Key/credentials.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': Api_Key["Firebase_URL"]
    })
    firebase_db = db.reference('messages')
    print("Firebase initialized")
    return firebase_db
    
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
    if lang == "hi":
        text_to_speech(destination.replace('_'," ") + " yaha se " + distance[:-3] + " kilometers dhur hai.")
    else:
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
    for tag in trav.find_all(['h3']):
        for a_tag in tag.find_all('a'):
            if len(a_tag.text)>10:
                news.append(a_tag.text)
    random.shuffle(news)
        
    return '.\n'.join(news[0:3])
            
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

def play_wake_sound(reverse):
    pygame.init()
    if reverse:
        pygame.mixer.music.load("temp/wake.wav")
    else:
        pygame.mixer.music.load("temp/wake_reverse.wav")
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
    firebase_db = initialize_Firebase()
    assistant = Recorder()
    print("You may now speak")
    while True:
        try:
            assistant.listen(None)
            wake_word = speech_to_text("temp/temp_audio.wav")
            # wake_word = input("Enter text to convert to speech: ") #voice command
            # if False:
            if ("eva" in wake_word.casefold()):
                while True:
                    play_wake_sound(False)
                    print("Listening...")
                    res = assistant.listen(INACTIVE_TIME)
                    if not res: 
                        break
                    message = speech_to_text("temp/temp_audio.wav")
                    # message = input("Enter prompt: ") #voice command
                    if ("namaste" in message.casefold()):
                        firebase_db.push().set({
                            'message': "namaste",
                            'timestamp': int(time.time())
                        })
                    elif (("path" in message.casefold()) or ("route" in message.casefold())  or ("rasta" in message.casefold())):        
                        lang = "en"
                        if ("rasta" in message.casefold()):
                            lang = "hi"   
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
        except:
            play_wake_sound(True)
            text_to_speech("Sorry, I don't know about that")