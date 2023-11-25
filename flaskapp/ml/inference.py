import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json
from os.path import dirname

model_path_group = "Nyarlat/text2group"
model_path_themes = "Nyarlat/text2topic"

group_tokenizer = AutoTokenizer.from_pretrained(model_path_group)
group_model = AutoModelForSequenceClassification.from_pretrained(model_path_group)

themes_tokenizer = AutoTokenizer.from_pretrained(model_path_themes)
themes_model = AutoModelForSequenceClassification.from_pretrained(model_path_themes)


def predict_group(text: str):
    with open('helpers\\label2id_group.json', 'r') as json_file:
        label2id = json.load(json_file)

    with open('helpers\\id2label_group.json', 'r') as json_file:
        id2label = json.load(json_file)

    tokens = group_tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        outputs = group_model(**tokens)

    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

    predicted_class_idx = torch.argmax(probs[0]).item()

    return id2label[str(predicted_class_idx)]


def predict_theme(text: str, predicted_group: str):
    with open('flaskapp/ml/helpers/label2id_theme.json', 'r') as json_file:
        label2id = json.load(json_file)

    with open('flaskapp/ml/helpers/id2label_theme.json', 'r') as json_file:
        id2label = json.load(json_file)

    text = predicted_group + text + predicted_group

    tokens = group_tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        outputs = group_model(**tokens)

    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

    predicted_class_idx = torch.argmax(probs[0]).item()

    return id2label[str(predicted_class_idx)]