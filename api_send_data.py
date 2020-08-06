import requests
import json
import pandas as pd
from database import send_data
from urllib import request
import os


def send_ingredients():
    f = open('output.txt','r')
    f = f.read().split('\n')
    
    for i in range(f.count('')):
        f.remove('')
    
    for i in range(len(f)):
        f[i] = f[i].split('\t')
        for j in range(f[i].count('')):
            f[i].remove('')
    
    data = pd.DataFrame(f)
    
    data = data.rename(columns={0:'idingredients'})
    
    for i in range(len(data)):
        data['idingredients'][i] = data['idingredients'][i].lower()
    
    
    df = data
    for i in df.index:
            try:
                t = pd.DataFrame()
                t =t.append(df.loc[i])
                t.reset_index(drop=True, inplace=True)
                try:
                   
                    test =t.loc[0].to_json()
                    send_data(test,'ingredients')
                    print('Data sent')
                   
                except:
                    test =t.loc[0].to_json()
                    send_data(test,'ingredients')
                    
            except Exception as e:
                print(e)

def send_recepies():

    url = "https://mycookbook-io1.p.rapidapi.com/recipes/rapidapi"
    
    payload = "https://www.jamieoliver.com/recipes/curry-recipes/veggie-korma/"
    headers = {
        'x-rapidapi-host': "mycookbook-io1.p.rapidapi.com",
        'x-rapidapi-key': "da82fa0637msh1349f7e56ed5543p173437jsn43981e323b74",
        'content-type': "text/plain",
        'accept': "text/plain"
        }
    
    response = requests.request("POST", url, data=payload, headers=headers)
    
    
    j = json.loads(response.text)
    send_data(j[0],'recepie')

send_recepies()
    

