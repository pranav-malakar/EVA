import openai
import json
import requests
import time
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import playsound
from gtts import gTTS
import os

key_Path = "Api_Key/Api_Key.json"
file = open(key_Path)
Api_Key = json.load(file)

# Set up OpenAI API key
openai.api_key = Api_Key["Gpt_Key"]

chat_log = [{'role': 'user', 'content': "Imagine you are a humanoid and your name is EVA. You are a virtual assitant to help people. You are a spohisticated humanoid robot capable of serving both as an Autnomous Professor and a Vistor Assitant with the help of latest AI techonology. You are created by students from SRM Institue of Science and Technology. SRM Institue of Science and Technology is one of the top ranking universities of India located in Kattankulathur, Chengalpattu, Tamil Nadu India. You can perform path planning, autonomous navigation, interactive presentation reading, speech recognition, object detection, face detection. You have a 4-wheeled omni-directional drive system and use ROS2."}]

def generate_text(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful voice assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the generated text from the response
    generated_text = response.choices[0].message.content
    return generated_text

def record_speech(duration, sample_rate=16000):
    print("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    return recording

def save_wav(audio_data, filename, sample_rate):
    sf.write(filename, audio_data, sample_rate)

def speech_to_text(audiofile):
    rec = sr.Recognizer()
    with sr.AudioFile(audiofile) as source:
        audio = rec.record(source)

    try:
        text = rec.recognize_google(audio)
    except sr.UnknownValueError:
        text = ""
    return text

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "temp.mp3"
    tts.save(filename)
    while True:
        try:
            playsound.playsound(filename)
            break
        except:
            continue
    os.remove(filename)

while True:
    
    # Record speech for 5 seconds
    record_duration = 5
    sample_rate = 16000
    audio_data = record_speech(record_duration, sample_rate)
    audiofile = "speech_recording.wav"
    save_wav(audio_data, audiofile, sample_rate)

    # Convert recorded speech to text
    user_message = speech_to_text(audiofile)
    print("Input Text: ", user_message)
    user_message= user_message + "Limit response to 50 words."

    if user_message.lower == "quit":
        break
    else:
        chat_log.append({"role":"user", "content":user_message})
        response = openai.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = chat_log
        )
        assitant_response = response.choices[0].message.content
        print("EVA:",assitant_response.strip("\n").strip())
        speak(assitant_response.strip("\n").strip())
        chat_log.append({"role":"assistant","content":assitant_response.strip("\n").strip()})
        
    time.sleep(1)