from app import app, db
from flask import render_template, flash, request, redirect, session, send_file, send_from_directory
from functools import wraps

import pandas as pd
import numpy as np

import torch
from transformers import BertTokenizer
# from pytorch_transformers import *

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

from collections import Counter
from datetime import datetime
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

        return {'htmlresponse':render_template('stock-data.html', graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON, graph4JSON=graph4JSON, df=df, stock=session['stock'])}


@app.route('/sentiment', methods={'GET', 'POST'})
@login_required
def sentiment():
    fd = FinanceData()
    stocks = fd.fetchTickers()
    first_name = session['user']['name'].split(" ")[0]

    form = ModelForm()
    form.stock.choices = [i for i in stocks]

    print(psutil.Process(os.getpid()).memory_info())
   
    return render_template('sentiment.html', form=form, first_name=first_name)


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        stock = request.form['stock']

        # Loading the stock tickers and saving them to a variable
        fd = FinanceData()
        stocks = fd.fetchTickers()
        
        # Saving the tick and tock name into session variables
        session['stock_ticker'] = stock
        session['stock_name'] = stocks.get(stock)
        class_names = ['negative', 'neutral', 'positive']

        # Initializing the tokenizer
        tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
        # tokenizer = tokenizer_class.from_pretrained(pretrained_weights)

        # Instantiating the twiiter data class to beging retrieving the tweet data
        td = TwitterData(session['stock_ticker'], session['stock_name'])
        df = td.getTweetData()
        

        # if not (os.path.isfile(f'app/static/data/{session["stock_name"]}_data.csv')):
        #     if df.empty:
        #         # return {'htmlresponse': render_template('404.html')}
        #         pass
        #     else:
        #         data = te.preprocess(df)
        # else:
        #     df = pd.read_csv(f'app/static/data/{session["stock_name"]}_Data.csv', sep='|')
        #     data = te.preprocess(df)

    
        df = pd.read_csv('app/static/data/3M_data.csv', sep='|')
        df = df[:100]

        total_tweets = len(df)
        seqlen = df['text'].apply(lambda x: len(x.split()))
        seqlen_max = df['text'].apply(lambda x: len(x.split())).max()

        # Load the model from state_dict
        model = SentimentClassifier(3)
        model.load_state_dict(torch.load('./transformer_model/trained_models/my_state'))
        model.eval()

        data_loader = create_data_loader(df, tokenizer, seqlen_max, 64)
        texts, predictions, prediction_probs = get_sentiment(model, data_loader)

        values, counts = np.unique(predictions, return_counts=True)
        occurence_count = Counter(predictions.tolist())
        sentiment = class_names[occurence_count.most_common(1)[0][0]]
        # data['sentiment'] = sentiment_lst
        # data.to_csv('transformer_model/data/Twitter_Data_bal_short_preds.csv')

        
        labels = ['distplot'] # name of the dataset
        fig5 = ff.create_distplot([seqlen], labels)
        fig5.update_xaxes(title='Token Count')
        fig5.update_yaxes(title='Density')
        graph5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)


        fig6 = go.Figure(data=[go.Bar(x=class_names, y=counts,
            hovertext=['27% market share', '24% market share', '19% market share'])])
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
    path = 'static/data/'+ session["stock_name"]+ '_data.csv'
    return send_file(path,
                     mimetype='text/csv',
                     attachment_filename= session["stock_name"]+'_data.csv',
                     as_attachment=True)


@app.route('/register')
def register():
    
    return render_template('register.html')


@app.route('/')
def login():
    
    print(psutil.Process(os.getpid()).memory_info())

    return render_template('login.html')