import firebase_admin
from firebase_admin import credentials, db
import time
import json

key_Path = "Api_Key/Api_Key.json"
file = open(key_Path)
Api_Key = json.load(file)

cred = credentials.Certificate("Api_Key/credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': Api_Key["Firebase_URL"]
})
ref = db.reference('messages')

def fetch_last_message():
    last_message = None
    last_message_key = None
    for key, val in ref.get().items():
        last_message = val
        last_message_key = key
    return last_message, last_message_key

while True:
    if len(ref.get())>1:
        last_message, last_message_key = fetch_last_message()
        if last_message:
            print("Message Recieved:", last_message["message"])
            ref.child(last_message_key).delete()
        else:
            print("No messages found.")
    print("Searching")
    time.sleep(1)
