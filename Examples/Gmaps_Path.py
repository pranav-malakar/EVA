import googlemaps
import requests
from PIL import Image
from io import BytesIO
import time
import json

key_Path = "Api_Key/Api_Key.json"
file = open(key_Path)
Api_Key = json.load(file)

gmaps = googlemaps.Client(key = Api_Key["Gmaps_Key"])

places_Cooridnaates = {
    "University_Building": (12.823430225414375, 80.04281426852602),
    "Tech_Park": (12.82487589069175, 80.04510017461834),
    "M_Block_Hostel": (12.820705752096051, 80.04595180253014),
    "Hi_Tech" :(12.821017799935602, 80.03892152308431)
}


def get_route_image_and_distance(start_coords, end_coords, api_key):
    
    # Convert coordinates to string format
    start = f"{start_coords[0]},{start_coords[1]}"
    end = f"{end_coords[0]},{end_coords[1]}"

    directions = gmaps.directions(start, end, mode="walking")
    polyline = directions[0]['overview_polyline']['points']
    walking_distance = directions[0]['legs'][0]['distance']['text']

    # Generate the URL for the static map with the route
    map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=600x400&path=enc:{polyline}&key={api_key}"

    # Download the image
    response = requests.get(map_url)
    image = Image.open(BytesIO(response.content))

    image_filename = f"temp/temp_path.png"
    image.save(image_filename)

    return walking_distance

walking_distance = get_route_image_and_distance(places_Cooridnaates["Hi_Tech"], places_Cooridnaates["University_Building"], Api_Key["Gmaps_Key"])
print("Walking distance:", walking_distance)
