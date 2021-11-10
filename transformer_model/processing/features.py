import pandas as pd


# Read the data from the CSV
data = pd.read_csv('app/static/data/Twitter_Data.csv', sep=',')


class Preproccess:

    def __init__(self, data):
        self.data = data


    def remove_null(self):
        # Remove the rows with missing values
        self.data = self.data.dropna()
    

    def convert_cat_vals(self):
        self.data['category'] = self.data['category'].apply(lambda x: 2 if x == 1 else (1 if x == 0 else 0))


    def get_seq_len(self):
        # Convert the rows into tokens (Splitting into words)
        seqlen = self.data['clean_text'].apply(lambda x: len(x.split()))
        return seqlen.max()