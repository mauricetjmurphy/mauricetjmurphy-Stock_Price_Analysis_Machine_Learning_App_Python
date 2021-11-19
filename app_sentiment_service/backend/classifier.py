from torch import nn
from transformers import BertModel
from sklearn.model_selection import train_test_split



# Constants
DEVICE = 'cpu'
SEQ_LEN = 32
BATCH_SIZE = 16
EPOCHS = 5
CLASS_NAMES = ['negative', 'neutral', 'positive']

class SentimentClassifier(nn.Module):

    bert_model = BertModel.from_pretrained('bert-base-uncased')

    def __init__(self, n_classes):
        super(SentimentClassifier, self).__init__()
        self.bert = self.bert_model
        self.drop = nn.Dropout(p=0.3)
        self.out = nn.Linear(self.bert.config.hidden_size, n_classes)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, input_ids, attention_mask):
        _, pooled_output, = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask, 
            return_dict=False
        )
        output = self.drop(pooled_output)
        output = self.out(output)
        return self.softmax(output)








 