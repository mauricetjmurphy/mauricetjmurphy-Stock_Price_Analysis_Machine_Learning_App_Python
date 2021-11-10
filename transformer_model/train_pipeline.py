import torch
from torch import nn
import pandas as pd
import numpy as np
from transformers import BertModel, BertTokenizer, AdamW, get_linear_schedule_with_warmup
from sklearn.model_selection import train_test_split
from transformer_model.processing.token_encoder import TokenEncoder as te
from collections import defaultdict


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



def train_epoch(model,data,loss_fn,optimizer,device,scheduler,n_examples):
    model = model.train()

    losses = []
    correct_predictions = 0

    for d in data:
        input_ids = d['input_ids']
        attention_mask = d['attention_mask']
        targets = d['targets']

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        _, preds = torch.max(outputs, dim=1)
        loss = loss_fn(outputs, targets)

        correct_predictions += torch.sum(preds == targets)
        losses.append(loss.item())

        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()

    return correct_predictions.double() / n_examples, np.mean(losses)


def eval_model(model, data, loss_fn, device, n_examples):
    model = model.eval()

    losses = []
    correct_predictions = 0

    with torch.no_grad():
        for d in data:
            input_ids = d['input_ids']
            attention_mask = d['attention_mask']
            targets = d['targets']

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

            _, preds = torch.max(outputs, dim=1)
            loss = loss_fn(outputs, targets)

            correct_predictions += torch.sum(preds == targets)
            losses.append(loss.item())

    return correct_predictions.double() / n_examples, np.mean(losses)

def run_training():
    history = defaultdict(list)
    best_accuracy = 0
    model = SentimentClassifier(len(CLASS_NAMES))

    tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

    # Read the data from the CSV
    data = pd.read_csv('app/static/data/Twitter_Data.csv', sep=',')

    # Split the data
    train, test = train_test_split(data, test_size = 0.2, random_state = 42)
    val, val_test = train_test_split(test, test_size = 0.5, random_state = 42)   

    train_data_loader = te.data_loader(train, tokenizer, SEQ_LEN, BATCH_SIZE)
    val_data_loader = te.data_loader(val, tokenizer, SEQ_LEN, BATCH_SIZE)
    test_data_loader = te.data_loader(test, tokenizer, SEQ_LEN, BATCH_SIZE)

    optimizer = AdamW(model.parameters(), lr=2e-5, correct_bias=False)
    total_steps = len(train_data_loader) * EPOCHS
    scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=20,
    num_training_steps=total_steps
    )
    loss_fn = nn.CrossEntropyLoss()

    for epoch in range(EPOCHS):
        print(f'Epoch {epoch +1}/{EPOCHS}')
        print('_'*10)

        train_acc, train_loss = train_epoch(
            model,
            train_data_loader,
            loss_fn,
            optimizer,
            DEVICE,
            scheduler,
            len(train)
        )

        print(f'Train loss {train_loss} Accuracy {train_acc}')

        val_acc, val_loss = eval_model(
            model,
            val_data_loader,
            loss_fn,
            DEVICE,
            len(train)
        )

        print(f'Val loss {val_loss} Val accuracy {val_acc}')
        print()

        history['train_acc'].append(train_acc)
        history['train_loss'].append(train_loss)
        
        history['val_acc'].append(val_acc)
        history['val_loss'].append(val_loss)

        if val_acc > best_accuracy:
            torch.save(model, 'model.pth')
            torch.save(model.state_dict(), 'my_state')
            best_accuracy = val_acc





 