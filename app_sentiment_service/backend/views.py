from rest_framework import permissions
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Predictions
from backend.serializers import PredictionSerializer
from backend.models import Predictions

from .predict import get_sentiment, create_data_loader
from .classifier import SentimentClassifier

import torch
from transformers import BertTokenizer

from collections import Counter
import pandas as pd
import numpy as np


@api_view(['GET'])
def getPredictions(request):
    tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
    class_names = ['negative', 'neutral', 'positive']
    
    df = pd.read_csv('./backend/data/3M_data.csv', sep='|')
    df = df[:128]

    total_tweets = len(df)
    seqlen = df['text'].apply(lambda x: len(x.split()))
    seqlen_max = df['text'].apply(lambda x: len(x.split())).max()

    # Load the model from state_dict
    model = SentimentClassifier(3)
    model.load_state_dict(torch.load('./backend/model/my_state'))
    model.eval()

    data_loader = create_data_loader(df, tokenizer, seqlen_max, 64)
    texts, predictions, prediction_probs = get_sentiment(model, data_loader)

    values, counts = np.unique(predictions, return_counts=True)
    occurence_count = Counter(predictions.tolist())
    sentiment = class_names[occurence_count.most_common(1)[0][0]]
    df['sentiment'] = predictions
    # data.to_csv('transformer_model/data/Twitter_Data_bal_short_preds.csv')

    # serializer = ProductSerializer(products, many=True)
    return Response({"prediction": sentiment, "tweet count": total_tweets, "seqlen": seqlen, "class names": class_names, "counts": counts,  'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods":
                    "GET,PUT,POST,DELETE,PATCH,OPTIONS",
            }})