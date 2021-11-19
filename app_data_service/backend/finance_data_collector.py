import pandas as pd
import numpy as np
import yfinance as yf
import pickle
import requests


class FinanceData:
    def __init__(self, ticker=None):
        self.ticker = ticker
   

    def fetchTickers(self):
        pickle_in = open('app/static/data/stocks.pkl', 'rb')
        stocks = pickle.load(pickle_in)
        return stocks
       

    def fetchStockData(self, startdate, enddate):
        # Getting data from yahoo finance with yahoo finance API 
        data = yf.download(self.ticker, startdate, enddate)
        return data


    def recommendations():
        pickle_in = open('app/static/data/stocks.pkl', 'rb')
        stocks = pickle.load(pickle_in)
        recommendations = []

        for ticker in stocks:
            pre_url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'
            post_url = '?formatted=true&crumb=svg7qs5y9UP&land=en-US&region=US&modules=upgradeDowngradeHistory,recommendationTrend,financialData, earningsHistory, earningsTrend&corsDomain=finance.yahoo.com'

            url = pre_url + ticker + post_url
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            res = requests.get(url, headers=headers)
            
            # If the url does not exist
            if not res.ok:
                recommendation = None

            try:
                result = res.json()['quoteSummary']['result'][0]
                recommendation_mean = result['financialData']['recommendationMean']['fmt']
                recommendation = result['financialData']['recommendationKey']
            except Exception as e:
                print(e)
                recommendation = None
                recommendation_mean = None

            if (recommendation != None):
                recommendations.append({'ticker': ticker, 'recommendation mean': recommendation_mean, 'recommendation': recommendation})
                
        return sorted(recommendations, key=lambda d: d['recommendation'], reverse=True)[:10]




