from app import app, db
from flask import render_template, flash, request, redirect, session, send_file, send_from_directory
from functools import wraps

from sklearn.linear_model import LinearRegression

import pandas as pd
import pandas_ta as ta
import numpy as np

import torch
from transformers import BertTokenizer

import plotly
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly_express as px

from .forms import StockForm
from .forms import ModelForm

from app.user import routes

from data_collector.finance_data_collector import FinanceData
from data_collector.twitter_data_collector import TwitterData
from transformer_model.processing.token_encoder import create_data_loader
from transformer_model.train_pipeline import SentimentClassifier
from transformer_model.predict import get_sentiment

from regression_model.regression import Regression

from collections import Counter
from datetime import datetime, date
import pickle
import json
import os.path

import os
import psutil
import gc
import time



# Decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap



@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/data', methods={'GET', 'POST'})
@login_required
def data():
    session['stock'] = 'MMM'
    session['from_date'] = pd.to_datetime('2018-07-15')
    session['to_date'] = pd.to_datetime(datetime.today())
    first_name = session['user']['name'].split(" ")[0]
   
    fd = FinanceData(session['stock'])
    stocks = fd.fetchTickers()

    form = StockForm()
    form.stock.choices = [i for i in stocks]

    gc.collect()
    print(psutil.Process(os.getpid()).memory_info())
    
    return render_template('index.html', form=form, stock='', first_name=first_name)


@app.route('/getStockData', methods=['GET', 'POST'])
def get_stock_data():
    if request.method == 'POST':
        
        stock = request.form['stock']
        from_date = request.form['from_date']
        to_date = request.form['to_date']
        session['stock'] = stock.split(", ")[0]
        session['from_date'] = pd.to_datetime(from_date)
        session['to_date'] = pd.to_datetime(to_date)
        
        fd = FinanceData(session['stock'])
        news = fd.fetchStockNews(stock)
        info = fd.fetchStockInfo(stock)

        try:
            df = fd.fetchStockData(session['from_date'] , session['to_date'])
        except Exception as e:
            print(e)

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=df.index, y=df['Close']))
        fig1.update_xaxes(rangeslider_visible=True, title='Date')
        fig1.update_yaxes(title='Stock Price (USD)')
        graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=df.index, y=df['Close']))
        fig2.add_trace(go.Scatter(x=df.index, y=df['Close']))
        fig2.update_xaxes( title='Date')
        fig2.update_yaxes(title='Stock Price (USD)')
        graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

        fig3 = go.Figure()
        fig3.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))
        fig3.update_layout(
        title='Candlestick chart',
        yaxis_title='Stock Price (USD per Share)'
        )
        graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

        fig4 = go.Figure()
        fig4.add_trace(go.Ohlc(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))
        fig4.add_trace(go.Scatter(x=df.index, y=df['Close'], line=dict(color='royalblue',width=1.5, dash='dot')))
        fig4.update_layout(
        title='Ohlc chart',
        yaxis_title='Stock Price (USD per Share)'
        )
        graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

        print(psutil.Process(os.getpid()).memory_info())

        return {'htmlresponse':render_template('stock-data.html', graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON, graph4JSON=graph4JSON, df=df, stock=session['stock'], news=news, info=info)}


@app.route('/regression', methods={'GET', 'POST'})
@login_required
def regression():
    fd = FinanceData(session['stock'])
    stocks = fd.fetchTickers()

    form = StockForm()
    form.stock.choices = [i for i in stocks]

    return render_template('regression.html', form=form)


@app.route('/regPredict', methods={'GET', 'POST'})
@login_required
def reg_predict():
    if request.method == 'POST':
    
        stock = request.form['stock']
        session['stock'] = stock.split(", ")[0]
        re = Regression()

        df, preds = re.reg_predict(stock)

        df.ta.ema(close='Adj Close', length=5, append=True)
        df = df.iloc[5:]
        preds_df = pd.DataFrame(preds, columns = ['Predicted Close']).iloc[5:]
        preds_df = preds_df.reset_index()
        df = df.reset_index()
        df = df.join(preds_df['Predicted Close'])

        fig1 = go.Figure()
        fig1.update_layout(autosize=False, width=1500, height=600)
        fig1.add_trace(go.Scatter(x=df.Date, y=df['Adj Close'], name="Adjusted Close"))
        fig1.add_trace(go.Scatter(x=df.Date, y=df['EMA_5'], name="Moving Average"))
        fig1.add_trace(go.Scatter(x=df.Date, y=df['Predicted Close'], name="Predicted Close"))
        fig1.update_xaxes(rangeslider_visible=True, title='Date')
        fig1.update_yaxes(title='Adj Close')
        graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        
        return {'htmlresponse':render_template('regression-data.html', graph7JSON=graph1JSON, df=df)}
      

@app.route('/sentiment', methods={'GET', 'POST'})
@login_required
def sentiment():
    fd = FinanceData()
    stocks = fd.fetchTickers()
    first_name = session['user']['name'].split(" ")[0]

    form = ModelForm()
    form.stock.choices = [i for i in stocks]
    form.percentage.choices = ['100%', '50%', '25%', '10%']

    print(psutil.Process(os.getpid()).memory_info())
   
    return render_template('sentiment.html', form=form, first_name=first_name)


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        stock = request.form['stock']
        percentage = int(''.join(request.form['percentage'].split('%')))

        # Loading the stock tickers and saving them to a variable
        fd = FinanceData()
        stocks = fd.fetchTickers()
        
        # Saving the tick and tock name into session variables
        session['stock_ticker'] = stock
        session['stock_name'] = stocks.get(stock)
        class_names = ['negative', 'neutral', 'positive']

        # Initializing the tokenizer
        tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
       
        seqlen = 0
        total_tweets = 0
        counts = []
        sentiment = ''
        df = pd.DataFrame()

        # Instantiating the twiiter data class to beging retrieving the tweet data
        td = TwitterData(session['stock_ticker'], session['stock_name'])
       

        if db.predictions.find_one({'stock': session['stock_name']}):
            stock_info = db.predictions.find_one({'stock': session['stock_name']})
            seqlen = stock_info['seqlen']
            seqs = stock_info['seqs']
            total_tweets = stock_info['total tweets']
            counts = stock_info['counts']
            sentiment = stock_info['sentiment']
        else:
            # df = pd.read_csv('app/static/data/3M_data.csv', sep='|')
            try:
                df = td.getTweetData(stock, session['stock_name'])
            except:
                df = pd.read_csv('app/static/data/3M_data.csv', sep='|')
                df = df[:2000]

            tweet_amount = round(len(df)/100)*percentage
            df = df[:tweet_amount]
            
            total_tweets = len(df)
            seqs = df['text'].apply(lambda x: len(x.split()))
            seqlen = df['text'].apply(lambda x: len(x.split())).max()

            # Load the model from state_dict
            model = SentimentClassifier(3)
            model.load_state_dict(torch.load('./transformer_model/trained_models/my_state'))
            model.eval()

            data_loader = create_data_loader(df, tokenizer, seqlen, 64)
            texts, predictions, prediction_probs = get_sentiment(model, data_loader)

            values, counts = np.unique(predictions, return_counts=True)
            occurence_count = Counter(predictions.tolist())
            sentiment = class_names[occurence_count.most_common(1)[0][0]]

            today = date.today()
            db.predictions.insert_one({"stock": session['stock_name'], "seqs": seqs.tolist(), "seqlen": seqlen.item(), "total tweets": total_tweets, "counts": counts.tolist(), "sentiment": sentiment, "date": today.strftime("%d/%m/%Y")})

        labels = ['distplot'] # name of the dataset
        fig5 = ff.create_distplot([seqs], labels)
        fig5.update_xaxes(title='Word Count')
        fig5.update_yaxes(title='Tweet Density')
        graph5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)

        fig6 = go.Figure(data=[go.Bar(x=class_names, y=counts)])
        colors = ['#eb4034','#e3820b', '#32a852']
        fig6.update_traces(marker_color=colors, marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
        fig6.update_xaxes(title='Twitter Sentiment')
        fig6.update_yaxes(title='Tweet Count')
        graph6JSON = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)

    return {'htmlresponse': render_template('sentiment-data.html',sentiment=sentiment, stock_name=session['stock_name'],total_tweets=total_tweets, graph5JSON=graph5JSON, graph6JSON=graph6JSON)}


@app.route('/getTweetCSV')
@login_required
def tweet_csv():
    path = 'static/data/data.csv'
    return send_file(path,
                     mimetype='text/csv',
                     attachment_filename = 'data.csv',
                     as_attachment=True)


@app.route('/register')
def register():
    
    return render_template('register.html')


@app.route('/')
def login():
    
    print(psutil.Process(os.getpid()).memory_info())

    return render_template('login.html')