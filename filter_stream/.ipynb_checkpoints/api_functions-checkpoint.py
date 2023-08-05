import requests
import os
import json
import pandas as pd
import csv

def set_token(path: str):
    """
    Desc: Set os env variable 'TOKEN' as bearer_token. 
    Params: 
        'path' - path to .json file containing developer account bearer_token value. 
    Pkgs: os, json
    """
    if path:
        creds = json.load(open(path))
        os.environ['TOKEN'] = creds['bearer_token']
    if os.environ['TOKEN']:
        return print('Set TOKEN enviroment varible.')
    else:
        Excption("Input 'path' to .json key file not found or is invalid.")
   
    
    
def bearer_auth(a):
    """
    Desc: Set authentication params for header. 
    Pkgs: os
    """
    a.headers["Authorization"] = "Bearer {}".format(os.environ['TOKEN'])
    a.headers["User-Agent"] = "v2FilteredStreamPython"
    
    return a


def add_rules(rule: str):
    """
    Desc: Add content filter rule to twitter API.
    Params:
        'rule' - rule to add to API filter.
    Helpers: bearer_auth()
    Pkgs: requests, json
    """
    stream_url = 'https://api.twitter.com/2/tweets/search/stream/rules'
    body = {"add":[{"value": rule}]}
    
    r = requests.post(url = stream_url,
                      auth = bearer_auth,
                      json = body,
                      timeout = 0.5
                     )
    
    if r.status_code != '200':
        Exception('STATUS: {} MESSAGE: {}'.format(r.status_code, r.text))
     
    response = r.json()
    r.close()
    
    return response



def list_rules(scope=None):
    """
    Desc: List content filter rules stored within twitter API.
    Params:
        'scope': 
            None - Returns list of both rule 'ids' and 'values' (Default).
            'ids' - Returns lsit of rule 'ids' only. 
            'values' - Returns list of rule 'values' only. 
    Helpers: bearer_auth()
    Pkgs: requests, json
    """
    if scope not in [None,'ids','values']:
        return Exception("'Scope' param value not valid.")
    
    stream_url = 'https://api.twitter.com/2/tweets/search/stream/rules'
    r = requests.get(url = stream_url,
                     auth = bearer_auth, 
                     timeout = 0.5
                    )
    
    if r.status_code != '200':
         Exception('STATUS: {} MESSAGE: {}'.format(r.status_code, r.text))
            
    if 'data' in r.json():
        output = r.json()['data']
        temp_list = []
        n_rules = len(output)
        r.close()
   
        if scope == None:
            return output

        elif scope == 'ids':
            for i in range(0, n_rules):
                temp_list.append(output[i]['id'])
            return temp_list

        else:
            for i in range(0, n_rules):
                temp_list.append(output[i]['value'])
            return temp_list
    else:
        r.close()
        return print('Rules list is empty.')
   

        
def delete_rules(ids: list):
    """
    Desc: Delete list of defined rules with twitter API content filter.
    Params: 
        'ids' - List of rule ids from twitter API to delete.
    Helpers: bearer_auth()
    Pkgs: requests, json
    """
    stream_url = 'https://api.twitter.com/2/tweets/search/stream/rules'
    body = {"delete":{"ids": ids}}
    r = requests.post(url = stream_url, 
                      auth = bearer_auth, 
                      json = body, 
                      timeout = 0.5)
    
    if r.status_code != '200':
         Exception('STATUS: {} MESSAGE: {}'.format(r.status_code, r.text))
    
    response = r.json()
    r.close()
    return response



def filter_stream(max_tweets=1):  
    print('starting...')
    stream_url = 'https://api.twitter.com/2/tweets/search/stream'
    max_tweets = max(1, max_tweets)
    print('about to stream...') 
    r = requests.get(url = stream_url,
                     auth = bearer_auth, 
                     stream = True
                    )
    
    print(r.text)
    if r.status_code != '200':
        Exception('MESSAGE: {}'.format(r.text))
    
    n_tweets = 0
    while n_tweets <= max_tweets:   
        print(n_tweets)
        for response_line in r.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                print(json.dumps(json_response, indent=4, sort_keys=True))
                n_tweets += 1
    
    print('closing.')
    r.close()