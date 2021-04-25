
import requests
import json
import pprint
import time
import config
import pandas as pd
from tqdm import tqdm


# users_listのimport
users_df = pd.read_csv('data/new_users.csv')
users_df.columns = ['user_id', 'users']

url = 'https://api.myanimelist.net/v2/users/@me/animelist?fields=list_status&limit=1000'
ACCESS_TOKEN = config.ACCESS_TOKEN
headers = {}
headers['Authorization'] = 'Bearer ' + ACCESS_TOKEN

def get_rates(users_index):
    url = 'https://api.myanimelist.net/v2/users/'+users_df.iloc[users_index]['users']+'/animelist?fields=list_status&limit=1000'
    response = requests.get(url, headers=headers)
    response = response.json()

    anime_list = response['data']
    anime_id_list = []
    rating_list = []
    for i in range(len(anime_list)):
        if anime_list[i]['list_status']['status'] == "completed":
            anime_id = anime_list[i]['node']['id']
            rating = anime_list[i]['list_status']['score']
            anime_id_list.append(anime_id)
            rating_list.append(rating)

    df = pd.DataFrame({'anime_id': anime_id_list,
                        'rating': rating_list})
    df['user_id'] = users_df.iloc[users_index]['user_id']
    df = df.reindex(columns=['user_id', 'anime_id', 'rating'])
    df.to_csv('data/ratings.csv', mode='a', index=False, header=None)

# headerだけの空リストを作成
empty_df = pd.DataFrame(np.random.randn(1,3), columns=['user_id', 'anime_id', 'rating'])
empty_df = empty_df[:0]
empty_df.to_csv('data/ratings.csv', index=False)

for i in tqdm(range(len(users_df))):
    try:
        get_rates(i)
    except Exception as e:
        print(e)
        print('\n\n time to sleep 30 seconds. \n')
        time.sleep(30)



