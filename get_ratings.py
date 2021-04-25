
import requests
import json
import pprint
import time
import pandas as pd
from tqdm import tqdm

# users_listのimport
users_df = pd.read_csv('data/new_users.csv')
users_df.columns = ['user_id', 'users']

url = 'https://api.myanimelist.net/v2/users/@me/animelist?fields=list_status&limit=1000'
ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjhiNjdjOGM5MGFhNDdmMWY5MDdmYTQ1NmZkODM1NGFiYzIwMWZhOTdiNzc2MzFiNDAxOTVmMGVkODc0YWU0MzJhNmZhOWU2NTNjMWUwM2QxIn0.eyJhdWQiOiJkYzk5NDVjYjgyZjRhMzg5MTI0N2Y2ZWZiNDlkMWQ5MiIsImp0aSI6IjhiNjdjOGM5MGFhNDdmMWY5MDdmYTQ1NmZkODM1NGFiYzIwMWZhOTdiNzc2MzFiNDAxOTVmMGVkODc0YWU0MzJhNmZhOWU2NTNjMWUwM2QxIiwiaWF0IjoxNjE5MTY2MjYwLCJuYmYiOjE2MTkxNjYyNjAsImV4cCI6MTYyMTc1ODI2MCwic3ViIjoiMTI2NDQzMjkiLCJzY29wZXMiOltdfQ.FoqEib7N4munklhA0tvv3rP-x5DUb-knRYR0eap44D4qAzUW4WaBNQCR8TWCiLijkpdWPRNFaUsskG7JeBgFMxv-CBUXi6qL70drxumk-9MxzA4tJ4V2B3uwXjoOtcvo8ZdxXl5CCYBQPzeuTabQwgYZLApIPOjUQBA0xxTqpKg-hRM9h3u11h9NClEiwg2Hi4mEpUaSXS3ZwVW2Wq3gXU-F_IedCOFUYAdt2IrT7zq5_RAUiAO0Y1Fln9YWV1KqfAHVBNWLipZe5SKJCY9eyXto8a_W5pRcwBB_4vXzUmwJd4dKwZ31HFuR8SmXmM5n-FAOvl8v1uvOXSfnxuMoDQ'
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
    df.to_csv('data/new_rating.csv', mode='a', index=False, header=None)

# headerだけの空リストを作成
empty_df = pd.DataFrame(np.random.randn(1,3), columns=['user_id', 'anime_id', 'rating'])
empty_df = empty_df[:0]
empty_df.to_csv('data/new_rating.csv', index=False)

for i in tqdm(range(len(users_df))):
    try:
        get_rates(i)
    except Exception as e:
        print(e)
        print('\n\n time to sleep 30 seconds. \n')
        time.sleep(30)



