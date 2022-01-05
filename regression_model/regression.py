import pandas as pd
import numpy as np
import yfinance as yf
import pickle
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

today = date.today()
pastdate = datetime.now() - relativedelta(days=21)


class Regression:
     def reg_predict(self, ticker):
          with open('regression_model/tained_models/regression_model', 'rb') as f:
               model = pickle.load(f)
               df = yf.download(ticker, pastdate, today.strftime("%Y-%m-%d"))
               df = df.dropna()
               preds = model.predict(df[['Adj Close']])
               return df, preds