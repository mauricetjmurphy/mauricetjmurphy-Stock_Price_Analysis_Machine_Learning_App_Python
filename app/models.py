from app import db
from datetime import datetime

class Recipe(db.Document):
    stock_name = mdb.StringField(max_length=300)
    seqlen = mdb.IntField()
    seqs = mdb.IntField()
    total_tweets = mdb.IntField()
    counts = mdb.ListField(mdb.IntField())
    sentiment = mdb.StringField(max_length=300)
    date_added = mdb.DateTimeField(default=datetime.utcnow)
