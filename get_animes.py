
import requests
import json
import pprint
import time
import config
import pandas as pd
from tqdm import tqdm

url = "https://api.myanimelist.net/v2/anime/"
# params = {'fields': ['id', 'title', 'genres', 'media_type', 'num_episodes', 'mean', 'num_list_users', 'start_date', 'start_season', 'source']}
ACCESS_TOKEN = config.ACCESS_TOKEN
params = {'fields': 'id, title, genres, media_type, num_episodes, mean, num_list_users, start_date, start_season, source'}
headers = {}
headers['Authorization'] = 'Bearer ' + ACCESS_TOKEN

def get_animes(anime_id, url=url):
    anime_id = str(anime_id)
    url = url + anime_id
    response = requests.get(url, params=params, headers=headers)
    response = response.json()
    pprint.pprint(response)

    if response != {'error': 'not_found', 'message': ''}:
        # main_pictureの削除
        del response['main_picture']

        # genre_listの結合
        genres = response['genres']
        genre_list = []
        for genre in genres:
            genre_list.append(genre['name'])
        re_genres = ','.join(genre_list)
        response['genres'] = re_genres

        # start_seasonの結合
        season = response['start_season']
        re_season = season['season'] + '_' + str(season['year'])
        response['start_season'] = re_season
        anime_list.append(response)

anime_list = []
for i in tqdm(range(1, 42_401)):
    try:
        get_animes(i)
    except Exception as e:
        print(e)
        print('\n\n time to sleep 30 seconds. \n')
        time.sleep(30)

# print(anime_list)

columns = ['anime_id', 'title', 'genres', 'media', 'episodes', 'rating', 'members', 'start_date', 'season', 'source']
anime_df = pd.DataFrame(anime_list)
anime_df.columns = columns
# headerだけの空csvを作成
empty_df = anime_df[:0]
empty_df.to_csv('data/new_anime.csv', index=False)
# 空csvにアニメのデータフレームを追記
anime_df.to_csv('data/new_anime.csv', mode='a',header=None ,index=False)

