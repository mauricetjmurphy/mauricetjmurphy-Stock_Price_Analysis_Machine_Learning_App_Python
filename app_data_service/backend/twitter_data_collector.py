from flask import send_file
import requests
import pandas as pd
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os


# Configuring the environment file 
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)


class TwitterData:
    # Assigning the environment variables
    api_key = os.environ.get("API_KEY")
    api_secret_key = os.environ.get("API_SECRET_KEY")
    bearer_token = os.environ.get("BEARER_TOKEN")
    # Twitter requires a standardised time format YY-MM-DDTHH:mm:ssZ
    dtformat = '%Y-%m-%dT%H:%M:%SZ'
    # Current time and date
    time = datetime.now()


    def __init__(self, ticker, stock_name, df=None):
        self.ticker = ticker
        self.stock_name = stock_name
        if df is None:
            # Assigning an empty dataframe to a variable
            self.df = pd.DataFrame()


    def saveToCSV(self, df):
        # Remove all the pipe chars from the data and save the file to csv
        df.replace('|', '', inplace=True)
        # Create a csv file with the data and its pipe seperated
        df.to_csv(f'app/static/data/{self.stock_name}_data.csv', sep='|', index=False)

    
    def getTweetData(self):
        # Setting up the Twitter tweet endpoint to gather tweet data
        tweet_endpoint = f'https://api.twitter.com/2/tweets/search/recent'
        headers = {'authorization': f'Bearer {self.bearer_token}'}
        params = {'tweet.fields': 'created_at,lang', 'max_results': '100'}

        # Modifing the query
        params['query'] = f'({self.stock_name} OR {self.ticker}) (lang:en)'

        for hour in range(24*7/2):
            print(f'Saving {hour} of 167')
            # All Twitter time is measured in UTC (Subtract 1 hour from GMT)
            pre60 = self.time - timedelta(minutes=120)
            time = self.time - timedelta(minutes=70)

            params['end_time'] = time.strftime(self.dtformat)
            params['start_time'] = pre60.strftime(self.dtformat)

            # Sending the request to the endpoint
            res = requests.get(tweet_endpoint, headers=headers, params=params)
            if res.status_code == 429:
                print('<------- TOO MANY REQUESTS (429) ------->')
                break
            
            time = pre60

            try:
                # Loop through the tweet data array and append each tweet to the empty dataframe
                for tweet in res.json()['data']:
                    try: 
                        self.df.append(tweet, ignore_index=True)
                    except Exception as e:
                        print(e)
                        pass
            except Exception as e:
                        print(e)
                        break
        if not self.df.empty:
            self.saveToCSV(self.df)
        return self.df
        

    def download_csv(stock_name):
        return send_file('static/data/tesla_tweets.csv',
                     mimetype='text/csv',
                     attachment_filename='tesla_tweets.csv',
                     as_attachment=True)
        



    
    









