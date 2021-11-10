import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer
# from transformer_model.config.core import config

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