import requests
import json
from bs4 import BeautifulSoup as BS
import re

def scrape_from_artist(artist_id, file_name='lyrics.txt'):
    base_url = "https://api.genius.com"
    path = 'artists/{}/songs'.format(artist_id)
    request_uri = '/'.join([base_url, path])

    # get artist
    r = requests.get(request_uri, headers=headers)
    print(r.text)

    r_json = json.loads(r.text)
    song_list = r_json['response']['songs']

    song_paths = []
    for x in song_list:
        song_paths.append(x['api_path'][1:])
    print(song_paths)

    for path in song_paths:
        scrape_from_song_path(path, file_name)

def scrape_from_song_path(song_path, file_name):
    base_url = 'https://genius.com'

    url = '/'.join([base_url, song_path])
    page = requests.get(url, headers=headers)

    soup = BS(page.content, 'html.parser')
    soup.prettify()

    # deal with both cases
    reg = re.compile('Lyrics__Container*')
    results_reg = soup.find_all('div', class_=reg)
    results = soup.find_all('div', class_='lyrics')

    # print(results_reg)
    # print(results)

    file = open(file_name, 'a')
    print(results_reg)
    print(results)
    for result in results_reg:
        file.write(result.text)
    for result in results:
        file.write(result.text)

    file.close()

client_id = "omA-SiO8cgdsN213wKZHtEX68I616aDwCuLxHtc19iVk5_S2CVzQhRGcJDLcn8bD"
client_secret = '_alNIfugH4WGqjgmtnNVlarITon53UYbxTLRYX0Lf3_Yglr-FkEyTmHxVi7QDDXiCYlaR451pNaXXt0KcwBaNg'
client_token = 'yzewkvDtjcS5FvLvrfUopskWKQk-miBMSZklLIs6cYbVLeIN03IShcX6bVb8cEeW'

token = 'Bearer {}'.format(client_token)
headers = {'Authorization' : token}

scrape_from_artist('1421', 'kendrick.txt')




