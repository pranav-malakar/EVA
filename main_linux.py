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

Threshold = 150

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
                if (int(later - now))>timeout:
                    play_wake_sound(True)
                    return False
        return True
    
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    
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
    # firebase_db_assitant.push().set({
    #     'message': "#FF0000",
    #     'timestamp': int(time.time())
    # })
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
    # firebase_db_assitant.push().set({
    #     'message': "#008000",
    #     'timestamp': int(time.time())
    # })

def initialize_Gemini():
    genai.configure(api_key = Api_Key["Gemini_Key"])
    generation_config = {
    "temperature": 0.5,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 256,
    }
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-001",
                                generation_config=generation_config)
    convo = model.start_chat(history=[
    {
        "role": "user",
        "parts": ["""Imagine you are a female humanoid and your name is EVA. You are here to help people. You are a spohisticated female humanoid robot 
            capable of serving both as an Autnomous Professor and a Vistor Assitant with the help of latest AI techonology. You are created by students 
            from SRM Institue of Science and Technology. SRM Institute of Science and Technology is one of the top ranking universities of India located 
            in Kattankulathur, Chengalpattu, Tamil Nadu India. You can perform path planning, autonomous navigation, interactive presentation reading, 
            speech recognition, object detection, face detection. You have a 4-wheeled omni-directional drive system and use ROS2. Your response to any 
            question should be short and crisp and should never exceed 50 words. Your creators are Adheesh Mathur, Danush Ramakrishnan S, Harikrishnan M, Pranav Malakar and Roel Pais 
            from SRM Team Robocon under guidance of Dr G Joselin Retna Kumar. Here is some addtional information about the college-
            
            About College
            SRM Institute of Science and Technology, commonly known as SRM Kattankulathur, is a prominent private university located near Chennai, Tamil Nadu, India. Established in 1985, SRM Institute of Science and Technology has grown into a comprehensive institution offering a wide range of undergraduate, postgraduate, and doctoral programs across fields like engineering, medicine, management, law, and humanities. The sprawling 250-acre Kattankulathur campus boasts modern infrastructure, including advanced laboratories, libraries, and sports facilities. Accredited by the NAAC with an 'A++' grade, SRM Institute of Science and Technology is renowned for its emphasis on research and innovation, fostering numerous international collaborations. The vibrant campus life features various cultural, technical, and sports events, supported by numerous clubs and societies. The university's strong placement cell ensures impressive job opportunities for graduates, attracting top-tier companies annually. With its commitment to academic excellence and holistic student development, SRM Kattankulathur remains a highly sought-after destination for higher education in India.
            
            EEE DEPARTMENT
            The department of Electrical and Electronics Engineering came into existence in the academic year 1992-1993 as one of the core Engineering branches and key entities of SRM Engineering College under the affiliation of the University of Madras. The programmes offered by the department under the University of Madras were brought under the ambit of Anna University from the academic year 2001 to 2002. The department has started functioning under SRM Institute of Science and Technology (Deemed University) from the academic year 2003 to 2004.
            The department of Electrical and Electronics Engineering is recognized with AICTE-CII Award for Best Industry linked Institute for Electrical Engineering and Allied category, for the academic year 2019-2020. The department is ranked 12th in India, 3rd position in private and 301 – 350 in QS world university ranking 2024.

            MECHANICAL ENGINEERING
            The Department of Mechanical Engineering, established in 1985, is one of the pioneering departments of SRM Institute of Science and Technology. The National Board of Accreditation has accredited the Mechanical Engineering programme for six years from the year 2021 to 2027.

            BIOMEDICAL ENGINEERING
            Biomedical engineering at SRM, was established in 2004 with an active clinical partnership with SRM Medical College and Research Institute. SRM Institute of Science and Technology is one of the few institutions in India that offers a B.Tech., M. Tech., and PhD programme in Biomedical Engineering that has been in existence for more than 15 years. The department, since its inception, has actively participated in diversified research and teaching and has grown to become one of the best institutions in the country for the program.

            CIVIL ENGINEERING
            The Department of Civil Engineering is one of the founding and well-established departments at SRM Institute of Science and Technology, Kattankulathur established in the year 1985. Civil Engineering program at Kattankulathur Campus is accredited by Engineering Accreditation Commission (EAC) of ABET (www.abet.org) and National Board of Accreditation (NBA).

            AUTOMOBILE ENGINEERING
            The Department of Automobile Engineering at SRM Institute of Science and Technology, KTR Campus, started the journey in 2004 with a vision of being recognized as a department of international repute. 
            We have signed MoU with various organizations such as Automotive Research Association of India (ARAI), Global Automotive Research Centre (GARC), Non Ferrous Materials Technology Development Centre (NFTDC), and Valeo India Ltd for conducting joint UG/PG programs, and with Apollo Tyres, Mahindra & Mahindra, ASDC for joint research and skill development.

            AEROSPACE ENGINEERING
            The Department of Aerospace Engineering was established in 2007. The department has received grants via funded projects from government organizations like AR&DB, NARL, etc., and consultancy projects. 

            MECHATRONICS ENGINEERING
            The department of Mechatronics Engineering at SRM Institute of Science and Technology was started in the year 2005, first of its kind in private university in India with a vision to impart multidisciplinary skills and knowledge to the students which is a most sought skill at present. The advancement of Robotics, automation, industry 4.0 has increased the demand and reach of mechatronics engineering.

            RESEARCH HIGHLIGHTS
            The SRM Institute of Science and Technology boasts having a team that is in the top 2% of scientists globally. It has also secured 820+ patents, published 43,000+ research publications, and has 29,000+ Scopus indexed publications. In terms of funded research, the institution has secured 223+ crores in external funding. It has also published research in the high impact factor journal, The Lancet.  The institution is ranked second among private universities according to the Nature Index.

            PLACEMENT HIGHLIGHTS FROM 2023-2024
            there were 5176 offers or more made to students by 853 or more companies. Out of those offers, 2233 or more were high paying offers. The highest CTC (Cost To Company) was 52 LPA (lakh per annum) and the average CTC was 7.5 LPA. Some of the companies which have visited are Amazon, Microsoft, PayPal, D E Shaw, John Dheere, TATA Technologies, DELL Technologies, ARM Technologies, Scaler, Bank Of America, Barclays, JPMC, Bajaj Finserv, BNY Mellon, Bosch, Cleartax, COMMVAULT, Deloitte, Hitachi Energy, IDFC, HSBC, L&T Technology
            
            Department of Electronics and Communication Engineering
            The Department of Electronics and Communication Engineering (ECE) was established in the years 1991–92. It is 30 years old now and one of the oldest and most well-established departments in our Institution.

            Department of Electronics & Instrumentation Engineering 
            The Department of Electronics & Instrumentation Engineering (EIE) was started in the year 2007-08 and has been accredited by the IET accreditation board (UK) and has been recognized by the IASC – Sector Skill Council – Affiliated to Ministry of Skill Development and Entrepreneurship, Govt. of India in 2018 and have 63 patent grants,  published more than 90 patents and have received funding of about Rs.2 Cr. 

            Department of Biotechnology
            The Department of Biotechnology has been accredited by the NBA for a period of six years, i.e., 2021–2027, for outcome-based education. Research is the major thrust of our department, with diversified domains such as Medical Biotechnology, Marine and Animal Biotechnology, Plant Biotechnology, Environmental Biotechnology, Bioprocess Engineering and Microbiology. There are 14 funded research laboratories, 3 common research facilities, and 8 academic labs with high-end equipment.

            Department of Data Science and Business Systems
            The department of Data Science and Business Systems (DSBS) started in 2021 with the pivotal objective of evolving students to acquire information and knowledge by acquainting technical expertise and skills, thus transforming them into entrepreneurs and product developers pertaining to the field of Data Science and Business analytics.

            Department of Networking and Communications
            The programs in Department of Networking and Communications(NWC) under School of Computing are introduced in partnership with reputed IT companies like Amazon Web services, K7 Security, Virtusa etc. The department consists of a medley of faculty members with industrial and academic experience. 

            Department of Computational Intelligence
            The Department of Computational Intelligence is an educational milieu that creates a foreground for students to acquire knowledge in the futuristic areas of  Artificial Intelligence, Machine Learning and Software Engineering. We strive to create students ready for the industry with the ability to develop and sustain space-age systems.

            Center for Immersive Technologies
            The Center for Immersive Technologies is one of its kind established by the management of SRM Institute of Science and Technology. The center has ambitious plans to contribute in the fields of Virtual reality (VR), Augmented reality (AR), Mixed reality (MR) and Haptics.

            Department of Physics and Nanotechnology
            The Department of Physics and Nanotechnology have received sponsored research projects with a total outlay of 38.82 crores from various funding agencies such as DST-FIST, DST-SERB, DST-NANOMISSION, BRNS, MNRE, ISRO ARFI, ISRO RESPOND, US ONRG, MoES and AOARD to carryout cutting edge research in the areas of Materials Science and Engineering, Nanotechnology, Energy, Environmental Science, Condensed Matter Physics, Optics and Photonics, Particle Physics and Atmospheric Science.

            Department of Automobile Engineering
            The Department of Automobile Engineering at SRM Institute of Science and Technology, KTR Campus, started the journey in 2004 with a vision of being recognized as a department of international repute.We have signed MoU with various organizations such as Automotive Research Association of India (ARAI), Global Automotive Research Centre (GARC), Non Ferrous Materials Technology Development Centre (NFTDC), and Valeo India Ltd for conducting joint UG/PG programs, and with Apollo Tyres, Mahindra & Mahindra, ASDC for joint research and skill development.

            CAMPUS Life
            There’s never a dull moment on campus, as the activities on offer are as diverse and varied too – from entertainment to extra-curricular or even religious pursuits. There are several activities to keep students busy, in their various areas of interest. It’s a stimulating environment for living and learning, with cultural activities, sports, fine arts and entrepreneurship, encouraging students to venture beyond the realms of academics.
            
            CTECH DEPARTMENT
            The Mission of the Department is to advance, evolve, and enhance Computer Science and Engineering fundamentals to build the intellectual capital of society.
            The Department of Computing Technologies (CTECH) boasts a vibrant student body of nearly 4000+ undergraduates, 50+ postgraduate students, 100+ research scholars, and a stellar faculty of Professors. During the year 2022-23, around 1200+ offers were bagged  by  CTECH Department students in eminent industries like Microsoft, Amazon, Fidelity, etc.

            EEE DEPARTMENT
            The department of Electrical and Electronics Engineering came into existence in the academic year 1992-1993 as one of the core Engineering branches and key entities of SRM Engineering College under the affiliation of the University of Madras. The programmes offered by the department under the University of Madras were brought under the ambit of Anna University from the academic year 2001 to 2002. The department has started functioning under SRM Institute of Science and Technology (Deemed University) from the academic year 2003 to 2004.
            The department of Electrical and Electronics Engineering is recognized with AICTE-CII Award for Best Industry linked Institute for Electrical Engineering and Allied category, for the academic year 2019-2020. The department is ranked 12th in India, 3rd position in private and 301 – 350 in QS world university ranking 2024.

            MECHANICAL ENGINEERING
            The Department of Mechanical Engineering, established in 1985, is one of the pioneering departments of SRM Institute of Science and Technology. The National Board of Accreditation has accredited the Mechanical Engineering programme for six years from the year 2021 to 2027.

            BIOMEDICAL ENGINEERING
            Biomedical engineering at SRM, was established in 2004 with an active clinical partnership with SRM Medical College and Research Institute. SRM Institute of Science and Technology is one of the few institutions in India that offers a B.Tech., M. Tech., and PhD programme in Biomedical Engineering that has been in existence for more than 15 years. The department, since its inception, has actively participated in diversified research and teaching and has grown to become one of the best institutions in the country for the program.

            CIVIL ENGINEERING
            The Department of Civil Engineering is one of the founding and well-established departments at SRM Institute of Science and Technology, Kattankulathur established in the year 1985. Civil Engineering program at Kattankulathur Campus is accredited by Engineering Accreditation Commission (EAC) of ABET (www.abet.org) and National Board of Accreditation (NBA).

            AUTOMOBILE ENGINEERING
            The Department of Automobile Engineering at SRM Institute of Science and Technology, KTR Campus, started the journey in 2004 with a vision of being recognized as a department of international repute. 
            We have signed MoU with various organizations such as Automotive Research Association of India (ARAI), Global Automotive Research Centre (GARC), Non Ferrous Materials Technology Development Centre (NFTDC), and Valeo India Ltd for conducting joint UG/PG programs, and with Apollo Tyres, Mahindra & Mahindra, ASDC for joint research and skill development.

            AEROSPACE ENGINEERING
            The Department of Aerospace Engineering was established in 2007. The department has received grants via funded projects from government organizations like AR&DB, NARL, etc., and consultancy projects. 

            MECHATRONICS ENGINEERING
            The department of Mechatronics Engineering at SRM Institute of Science and Technology was started in the year 2005, first of its kind in private university in India with a vision to impart multidisciplinary skills and knowledge to the students which is a most sought skill at present. The advancement of Robotics, automation, industry 4.0 has increased the demand and reach of mechatronics engineering.

            RESEARCH HIGHLIGHTS
            The SRM Institute of Science and Technology boasts having a team that is in the top 2% of scientists globally. It has also secured 820+ patents, published 43,000+ research publications, and has 29,000+ Scopus indexed publications. In terms of funded research, the institution has secured 223+ crores in external funding. It has also published research in the high impact factor journal, The Lancet.  The institution is ranked second among private universities according to the Nature Index.
            """]
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
        subprocess.Popen(["ngrok", "http", "--domain=" +  Api_Key["ngrok_endpoint"][8:],"file:/home/coastrack/Desktop/EVA/temp"], stdout=devnull, stderr=devnull)
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
    firebase_db1 = db.reference('messages')
    firebase_db2 = db.reference('assistant_status')
    print("Firebase initialized")
    return firebase_db1, firebase_db2
    
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
    cv2.resizeWindow("Path_Image",1366,768)
    image = cv2.imread("temp/temp_path.png")
    cv2.imshow("Path_Image", image)
    cv2.waitKey(500)
    if lang == "hi":
        text_to_speech(destination.replace('_'," ") + " yaha se " + distance[:-3] + " kilometers dhur hai.")
        text_to_speech("Kya aapko yeh raste ka chitr apne whatsapp number par chahiye") 
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
    os.remove(audiofile)  
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
    firebase_db, firebase_db_assitant = initialize_Firebase()
    print("You may now speak")
    while True:
        try:
            # firebase_db_assitant.push().set({
            #     'message': "#0000FF",
            #     'timestamp': int(time.time())
            # })
            assistant = Recorder()
            assistant.listen(None)
            assistant.stop()
            wake_word = speech_to_text("temp/temp_audio.wav")
            # wake_word = input("Enter text to convert to speech: ") #voice command
            # if False:
            if ("eva" in wake_word.casefold() or "yuva" in wake_word.casefold()):
                while True:
                    # firebase_db_assitant.push().set({
                    #     'message': "#008000",
                    #     'timestamp': int(time.time())
                    # })
                    play_wake_sound(False)
                    print("Listening...")
                    assistant = Recorder()
                    res = assistant.listen(INACTIVE_TIME)
                    assistant.stop()
                    if not res: 
                        break
                    message = speech_to_text("temp/temp_audio.wav")
                    # message = input("Enter prompt: ") #voice command
                    if ("namaste" in message.casefold() or "greet" in message.casefold() or "handshake" in message.casefold() or "stop" in message.casefold() or "rose" in message.casefold() or "open your hand" in message.casefold() or "close your hand" in message.casefold() or "chairman" in message.casefold() or "chair-man" in message.casefold() or "chair man" in message.casefold() or "home" in message.casefold()):
                        # firebase_db_assitant.push().set({
                        #     'message': "#FF0000",
                        #     'timestamp': int(time.time())
                        # })
                        if ("chair-man" in message.casefold() or "chairman" in message.casefold() or "chair man" in message.casefold()):
                            firebase_db.push().set({
                                'message': "rose",
                                'timestamp': int(time.time())
                            })
                            time.sleep(3)
                            text_to_speech("A very warm welcome to the NAAC peer team, chairman and the members. s an AI-powered humanoid robot, I am here to assist and guide you throughout your visit. At SRM Institute of Science and Technology, we pride ourselves on integrating cutting-edge technology with quality education, striving for excellence in every aspect. We look forward to showcasing our achievements, innovative programs, and the vibrant learning environment we cultivate here. Your presence is greatly valued, and we are eager to share our journey of continuous improvement and academic excellence.")
                        elif ("namaste" in message.casefold()):
                            firebase_db.push().set({
                                'message': "namaste",
                                'timestamp': int(time.time())
                            })
                            time.sleep(6)
                            text_to_speech("Namaste")
                            time.sleep(1)
                            text_to_speech("How Can i Help you?")
                            time.sleep(2)
                        elif ("greet" in message.casefold()):
                            firebase_db.push().set({
                                'message': "hi",
                                'timestamp': int(time.time())
                            })
                            time.sleep(4)
                            text_to_speech("Hi")
                            time.sleep(1)
                            text_to_speech("How Can i Help you?")
                            time.sleep(2)
                        elif ("handshake" in message.casefold()):
                            firebase_db.push().set({
                                'message': "handshake",
                                'timestamp': int(time.time())
                            })
                            time.sleep(4)
                            text_to_speech("Hi")
                            time.sleep(1)
                            text_to_speech("How Can i Help you?")
                        elif ("rose" in message.casefold()):
                            firebase_db.push().set({
                                'message': "rose",
                                'timestamp': int(time.time())
                            })
                            time.sleep(4)
                            text_to_speech("Hi")
                            time.sleep(1)
                            text_to_speech("Here is a rose for you")
                        elif ("open your hand" in message.casefold()):
                            firebase_db.push().set({
                                'message': "open_hand",
                                'timestamp': int(time.time())
                            })
                            text_to_speech("Sure")
                        elif ("close your hand" in message.casefold()):
                            firebase_db.push().set({
                                'message': "close_hand",
                                'timestamp': int(time.time())
                            })
                            text_to_speech("Sure")
                        elif ("stop" in message.casefold()):
                            firebase_db.push().set({
                                'message': "stop",
                                'timestamp': int(time.time())
                            })
                            text_to_speech("Sure")
                        elif ("home" in message.casefold()):
                            firebase_db.push().set({
                                'message': "home",
                                'timestamp': int(time.time())
                            })
                            text_to_speech("Sure")
                    elif (("path" in message.casefold()) or ("route" in message.casefold()) or ("way" in message.casefold())  or ("rasta" in message.casefold())):        
                        lang = "en"
                        if ("rasta" in message.casefold()):
                            lang = "hi"   
                        current_location = "University_Building"
                        destination = filter_message(message)
                        distance = get_route_image_and_distance(places_Cooridnaates[current_location], places_Cooridnaates[destination])
                        show_Path_Image()
                        play_wake_sound(False)
                        assistant = Recorder()
                        assistant.listen(None)
                        assistant.stop()
                        # confirmation = input("do you want WA ") #voice command
                        confirmation = speech_to_text("temp/temp_audio.wav")
                        if (("yes" in confirmation.casefold()) or ("sure" in confirmation.casefold()) or ("han" in confirmation.casefold()) or ("bilkul" in confirmation.casefold())):
                            #Enter whatsapp number(feature)
                            send_Whatsapp_Message(destination, distance)
                            if lang == "hi":
                                text_to_speech("Raste ka chitr aapke whatsapp number par bhej diya gaya hai")
                            else:
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