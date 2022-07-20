#import requests
import os
import re
import requests
import json
import pandas as pd 


#sending request for server that fetch Broklyn 99 quotes 
def find_bnn_quote(qu):
    url = "https://brooklyn-nine-nine-quotes.p.rapidapi.com/api/v1/quotes/find"
    querystring = {"searchTerm":qu}

    headers = {
    "X-RapidAPI-Key": "c924fdabe1mshc45c61a520f2ecbp15f7a3jsna6203076037f",
    "X-RapidAPI-Host": "brooklyn-nine-nine-quotes.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    with open(f'results_brooklyn99/{qu}.json' , 'w+') as outfile:
        json.dump(response.text , outfile)  

def get_friends_quote(qu):
    output = [] 
    dirs = os.listdir('data')
    for season in dirs: 
        curr = os.listdir(f'data/{season}')
        for f in curr:
            curr_file = open(f'data/{season}/{f}' , "r" , encoding="utf8")
            readfile = curr_file.read()
            if re.search( qu , readfile , re.IGNORECASE or re.DOTALL ): 
                output.append(f'{f}')
            curr_file.close()

    #make csv with meta data
    season = map(lambda s :  s[0:2] , output)
    episode = map(lambda s : s[2:4] , output)
    df = pd.DataFrame()
    df['season'] = list(season)
    df['episode'] = list(episode)
    df['is offensive'] = ''
    df.to_csv(f'friends_csv/{qu}.csv' , index = False)
    
    #not relevant, old format
    #content = str(output)
    #freq = len(output)
    #result_file = open(f'results_friends/{qu}.txt' , 'w+' , encoding="utf8")
    #result_file.write(content + '\n' + str(freq))
    #result_file.close()     


def get_brnn_quote(qu):
    output = [] 
    dirs = os.listdir('bnn_data')
    for season in dirs: 
        curr = os.listdir(f'bnn_data/{season}')
        for f in curr:
            curr_file = open(f'bnn_data/{season}/{f}' , "r" , encoding="utf8")
            readfile = curr_file.read()
            if re.search( qu , readfile , re.IGNORECASE or re.DOTALL ): 
                output.append(f'{f}')
            curr_file.close()
        
    content = str(output)
    freq = len(output)
    result_file = open(f'results_brooklyn99/{qu}.txt' , 'w+' , encoding="utf8")
    result_file.write(content + '\n' + str(freq))
    result_file.close() 

def convert_to_cvs(): 
    dirs = os.listdir('bnn_jsons')
    for js in dirs: 
        with open(f'bnn_jsons/{js}', encoding='utf-8') as inputfile:
            jf = json.load(inputfile)
            df = pd.read_json(jf)
        df = df.drop([ 'PageNumber' ,'PageSize' , 'Message'] , axis = 1)
        df['is offensive'] = ''
        df.to_csv(f'bnn_csv/{js}.csv', index=False)
         

if __name__ == '__main__':
    offensive = [' fat ' , 'woman' ,'women' , 'girl' , 'slut' , 'gay' , 'lesbian' , 'penis' , 'our country' , 'foreign']
    for word in offensive:
        find_bnn_quote(word)
        get_friends_quote(word)
    convert_to_cvs()
    