from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Tuple

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

# pretrained finbert model - financial sentiment analysis transformer
tokenizer = AutoTokenizer.from_pretrained('ProsusAI/finbert')
model = AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert').to(device)
labels = ['positive', 'negative', 'neutral']

def estimate_sentiment(news):
    if news:
        tokens = tokenizer(news, return_tensors='pt', padding=True).to(device)
        result = model(tokens['input_ids'], attention_mask=tokens['attention_mask'])['logits']
        # scale to probability
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)
        probability = result[torch.argmax(result)]
        sentiment = labels[torch.argmax(result)]

        return probability, sentiment
    else:
        return 0, labels[-1]
    
# test inputs for finbert model
if __name__ == '__main__':
    probability_tensor, sentiment = estimate_sentiment(['markets responded postively to the company IPO! Looking promising!'])
    probability_tensor2, sentiment2 = estimate_sentiment(['Here is what you would have earned if you invested in Tesla 5 years ago'])
    print(probability_tensor, sentiment)
    print(probability_tensor2, sentiment2)
    print(torch.cuda.is_available())