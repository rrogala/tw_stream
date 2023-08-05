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
    
    
def sample_stream(max_tweets=1):  
    print('starting...')
    stream_url = 'https://api.twitter.com/2/tweets/sample/stream'
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
    
    
