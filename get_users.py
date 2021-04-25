
import requests
import json
import pprint
import time
import numpy as np
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

url = 'https://myanimelist.net/users.php?cat=user&q=&loc=&agelow=14&agehigh=34&g=&show='

def get_users(url, num):
    url = url + str(num)
    response = requests.get(url).text
    soup = bs(response, 'html.parser')
    items = soup.find_all(class_='borderClass')
    user_list = []
    for i in range(1,25):
        users = items[i].find('a').text
        user_list.append(users)
    # print(users_list)
    return user_list

users_list = []
for num in tqdm(range(0,108_001,24)):
    user_list = get_users(url, num)
    users_list.extend(user_list)
    time.sleep(3)

# print(users_list)
sr = pd.Series(users_list, name='users', index=np.arange(1,len(users_list)+1))
sr.to_csv('data/users.csv')

