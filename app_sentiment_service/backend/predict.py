import torch
from torch.utils.data import Dataset, DataLoader

class TokenEncoder(Dataset):
    
    def __init__(self, texts, tokenizer, max_len, targets=None):
        self.texts = texts
        self.targets = targets
        self.tokenizer = tokenizer
        self.max_len = max_len
  
    def __len__(self):
        return len(self.texts)
  
    def __getitem__(self, item):
        text = str(self.texts[item])
        target = []

        encoding = self.tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=self.max_len,
        return_token_type_ids=False,
        pad_to_max_length=True,
        return_attention_mask=True,
        return_tensors='pt',
        )

        return {
        'text': text,
        'input_ids': encoding['input_ids'].flatten(),
        'attention_mask': encoding['attention_mask'].flatten(),
        'targets': []
        }


def create_data_loader(df, tokenizer, max_len, batch_size):
    ds = TokenEncoder(
    texts=df.text.to_numpy(),
    targets=[],
    tokenizer=tokenizer,
    max_len=max_len
    )

    return DataLoader(
        ds,
        batch_size=batch_size,
        num_workers=4,
        drop_last=True,
    )

def get_sentiment(model, data):
    model = model.eval()

    texts = []
    predictions = []
    prediction_probs = []
    
    with torch.no_grad():
        for d in data:
            texts = d['text']
            input_ids = d['input_ids']
            attention_mask = d['attention_mask']
           
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

            _, preds = torch.max(outputs, dim=1)

            texts.extend(texts)
            predictions.extend(preds)
            prediction_probs.extend(outputs)
            
    predictions = torch.stack(predictions).cpu()
    prediction_probs = torch.stack(prediction_probs).cpu()

    return texts, predictions, prediction_probs