from twilio.rest import Client
import json

key_Path = "Api_Key/Api_Key.json"
file = open(key_Path)
Api_Key = json.load(file)

account_sid = Api_Key["Twilio_Account_SID"]
auth_token = Api_Key["Twilio_Authorization"]
client = Client(account_sid, auth_token)

destination = "M Block Hostel"
distance = "0.3 km"
message_body = "Hello, I'm EVA (Enhanced Virtual Assistant)! 🤖💫\n\nI'm a humanoid robot armed with cutting-edge AI technology. Here's the designated route to " + destination + " as per your request! 🗺️ \n\nIt's approximately " + distance + " away. 🚶‍♂️"

message = client.messages.create(
  from_ = Api_Key["Twilio_Whatsapp_No"],
  body = message_body,
  media_url = Api_Key["ngrok_endpoint"]+"/temp_path.png",
  to = Api_Key["Reciever_Whatsapp_No"]
)

print(message.sid)