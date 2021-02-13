import requests
import json
from bs4 import BeautifulSoup as BS
import re

base_url = "https://api.genius.com"
client_id = "omA-SiO8cgdsN213wKZHtEX68I616aDwCuLxHtc19iVk5_S2CVzQhRGcJDLcn8bD"
client_secret = '_alNIfugH4WGqjgmtnNVlarITon53UYbxTLRYX0Lf3_Yglr-FkEyTmHxVi7QDDXiCYlaR451pNaXXt0KcwBaNg'
client_token = 'yzewkvDtjcS5FvLvrfUopskWKQk-miBMSZklLIs6cYbVLeIN03IShcX6bVb8cEeW'

token = 'Bearer {}'.format(client_token)
headers = {'Authorization' : token}

artist_id = "1421"
path = 'artists/{}/songs'.format(artist_id)
request_uri = '/'.join([base_url, path])

r = requests.get(request_uri, headers=headers)
print(r.text)

r_json = json.loads(r.text)
song_list = r_json['response']['songs']

song_paths = []
for x in song_list:
    song_paths.append(x['api_path'][1:])
print(song_paths)

song_path = song_paths[0]
url = '/'.join(['https://genius.com', song_path])
page = requests.get(url, headers=headers)

soup = BS(page.content, 'html.parser')
soup.prettify()
print(soup.prettify())
reg = re.compile('Lyrics__Container*')
results_reg = soup.find_all('div', class_=reg)
results = soup.find_all('div', class_='lyrics')

print(results_reg)
print(results)

for x in results_reg:
    print(x.text)
for x in results:
    print(x.text)