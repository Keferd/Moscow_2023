from transformers import AutoTokenizer, AutoModel, DataCollatorWithPadding, AutoModelForSequenceClassification, TrainingArguments, Trainer
import pandas as pd
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split

import evaluate


df = pd.read_csv('output.csv', sep=';')
unique_labels = df['Тема'].unique()
label2id = {label: i for i, label in enumerate(unique_labels)}
id2label = {i: label for i, label in enumerate(unique_labels)}
df['Target'] = df['Тема'].map(label2id)
df.head(2)

tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny2")
rubert_model = AutoModelForSequenceClassification.from_pretrained("cointegrated/rubert-tiny2", num_labels=195, id2label=id2label, label2id=label2id)

X = list(df["Текст инцидента"])
y = list(df["Target"])
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2,stratify=y)
X_train_tokenized = tokenizer(X_train, padding=True, truncation=True, max_length=512)
X_val_tokenized = tokenizer(X_val, padding=True, truncation=True, max_length=512)

class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels=None):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        if self.labels:
            item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.encodings["input_ids"])

train_dataset = Dataset(X_train_tokenized, y_train)
val_dataset = Dataset(X_val_tokenized, y_val)

f1 = evaluate.load("f1")
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return f1.compute(predictions=predictions, references=labels, average='weighted')

rubert_model = rubert_model.to('cuda')

args = TrainingArguments(
    output_dir="rubert2_output_5",
    num_train_epochs=5,
    per_device_train_batch_size=64
)
trainer = Trainer(
    model=rubert_model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics
)

trainer.train()

trainer.evaluate()

model_path = "fine-tune-rubert-512tokens"
rubert_model.save_pretrained(model_path)
tokenizer.save_pretrained(model_path)