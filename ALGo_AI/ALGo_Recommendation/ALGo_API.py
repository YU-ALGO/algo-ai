from fastapi import FastAPI
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import pandas as pd
import numpy as np
from tensorflow.keras.models import Model, load_model
import gc

app = FastAPI()

data = pd.read_csv('User_Item_Rating.csv')
data_food = pd.read_csv('haccp_food_data.csv')

virtual_user = []
virtual_user_max_index = []
for i in range(1,10001):
    df = data[data['User'] == i]
    virtual_user_max_index.append(len(df))
    virtual_user.append(df[['Item','Rating']].values)
food_allergy = data_food[['소고기', '메밀', '닭', '조개류', '게', '난류', '생선', '과일', '마늘', '우유', '견과류', '돼지고기', '참깨', '새우', '대두', '오징어', '아황산류', '토마토', '채소', '밀']].values

food_list = np.arange(1,6261)
model = load_model('ALGo.h5')


def get_distance(i, new_user_max_index,user_item,user_rating):
    distance = 0
    virtual_index = 0
    new_index = 0
    while(True):
        if(virtual_index==virtual_user_max_index[i-1] and new_index==new_user_max_index):
            break;
        elif(new_index==new_user_max_index):
            distance += (virtual_user[i-1][virtual_index][1])**2
            virtual_index+=1
        elif(virtual_index==virtual_user_max_index[i-1]):
            distance += (user_rating[new_index])**2
            new_index+=1
        elif(virtual_user[i-1][virtual_index][0] == user_item[new_index]):
            distance += (virtual_user[i-1][virtual_index][1]-user_rating[new_index])**2
            virtual_index+=1
            new_index+=1
        elif(virtual_user[i-1][virtual_index][0]  < user_item[new_index]):
            distance += (virtual_user[i-1][virtual_index][1])**2
            virtual_index+=1
        elif(virtual_user[i-1][virtual_index][0]  > user_item[new_index]):
            distance += (user_rating[new_index])**2
            new_index+=1
    return distance

del data
del data_food
gc.collect()

@app.get("/recommend")
def read_item(allergy: str, favorites: str, recently_viewed: str):
    favorites = favorites[1:-1]
    recently_viewed = recently_viewed[1:-1]
    
    user_item = []
    user_favorite = []
    user_recently_viewed = []
    if favorites != '':
        for item in favorites.split(','):
            int_item = int(item)
            user_favorite.append(int_item)
            user_item.append(int_item)
    if recently_viewed != '':
        for item in recently_viewed.split(','):
            int_item = int(item)
            if(int_item not in user_favorite):
                user_recently_viewed.append(int_item)
                user_item.append(int_item)
    user_item.sort()
    user_rating = []
    for i in user_item:
        if i in user_favorite:
            user_rating.append(5)
        else:
            user_rating.append(1)
    recommendation = []
    new_user_max_index = len(user_item)
    min_distance = get_distance(1,new_user_max_index,user_item,user_rating)
    for i in range(2,10001):
        distance = get_distance(i,new_user_max_index,user_item,user_rating)
        if(distance<min_distance):
            similar_user = i
            min_distance = distance
    predictions = model.predict([np.full(6260,similar_user), food_list],verbose = 0)
    recommended_item_ids = (-predictions.reshape(6260,)).argsort()
    recommend_num = 5
    for i in recommended_item_ids:
        check = True
        for allergy_index in range(20):
            if(allergy[allergy_index]=='1' and food_allergy[i][allergy_index]):
                check = False
                break
        if(check and i not in user_item):
            recommendation.append(int(i))
            recommend_num-=1
            if(recommend_num == 0):
                break
    return {"item_id": recommendation}


