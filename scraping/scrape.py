import requests
import json
from bs4 import BeautifulSoup as BS
import re
import time
import os
from dotenv mport load_dotenv

def scrape_from_artist(artist_id, file_name='lyrics.txt'):
    initial_time = time.time()

    base_url = "https://api.genius.com"
    path = 'artists/{}/songs'.format(artist_id)
    request_uri = '/'.join([base_url, path])

    song_paths = []
    # get artist
    page_num = 1
    while True:
        params={'page' : page_num}
        r = requests.get(request_uri, headers=headers, params=params)

        r_json = json.loads(r.text)
        song_list = r_json['response']['songs']
        new_num = r_json['response']['next_page']

        for x in song_list:
            song_paths.append(x['api_path'][1:])
        print(song_list[-1])
        if not new_num:
            break
        print(new_num)
        page_num += 1

    num_songs = len(song_paths)
    for i, path in enumerate(song_paths):
        print("{}/{}".format(i, num_songs))
        scrape_from_song_path(path, file_name)

    print(time.time()-initial_time)

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


    file = open(file_name, 'a', encoding='utf-8')
    for result in results_reg:
        print("container")
        for br in result.find_all('br'):
            br.replace_with('\n')
        text = result.text.replace('\u2005', ' ')
        text = text.replace('\u205f', ' ')
        file.write(text)
        file.write('\n')
        print(repr(text))

    for result in results:
        print("not container")
        text = result.text.replace('\u2005', ' ')
        text = text.replace('\u205f', ' ')
        file.write(text)
        print(repr(text))
    file.write('\n')
    file.close()

load_dotenv()
client_id = os.getenv("CLIENTID")
client_secret = os.getenv("CLIENTSECRET")
client_token = os.getenv("CLIENTOKEN")

token = 'Bearer {}'.format(client_token)
headers = {'Authorization' : token}

scrape_from_artist('12418', 'EdSheeran.txt')




