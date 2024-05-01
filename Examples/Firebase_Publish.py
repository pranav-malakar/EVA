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

firebase_db = db.reference('messages')

while True:
    message = input("Enter message to publish: ")
    firebase_db.push().set({
        'message': message,
        'timestamp': int(time.time())
    })
