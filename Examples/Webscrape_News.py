from bs4 import BeautifulSoup as BS
import requests as req

url = "https://www.hindustantimes.com/topic/chennai"
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36'}

webpage = req.get(url, headers=headers)
trav = BS(webpage.content, "html.parser")

cnt = 0
for tag in trav.find_all(['h2','h3']):
    for a_tag in tag.find_all('a'):
        print(a_tag.text)
        cnt += 1
        
print(cnt)