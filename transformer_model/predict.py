import torch

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