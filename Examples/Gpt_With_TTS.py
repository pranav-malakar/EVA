import openai
from gtts import gTTS
import os
import playsound
import json

key_Path = "Api_Key/Api_Key.json"
file = open(key_Path)
Api_Key = json.load(file)

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

openai.api_key = Api_Key["Gpt_Key"]

chat_log = [{'role': 'user', 'content': "Imagine you are a humanoid and your name is EVA. You are a virtual assitant to help people."}]

while True:
    print("User: ",end="")
    user_message = input()
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
