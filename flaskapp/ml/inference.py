import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json
from os.path import dirname
from preprocessing import soft_remove

model_path_group = "Nyarlat/text2groupV2"
model_path_themes = "Nyarlat/text2topicV2"

group_tokenizer = AutoTokenizer.from_pretrained(model_path_group, token="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")
group_model = AutoModelForSequenceClassification.from_pretrained(model_path_group, token="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")

themes_tokenizer = AutoTokenizer.from_pretrained(model_path_themes, token="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")
themes_model = AutoModelForSequenceClassification.from_pretrained(model_path_themes, token="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")


def predict_group(text: str):
    text = soft_remove(text)
    with open('ml/helpers/label2id_group.json', 'r') as json_file:
        label2id = json.load(json_file)

    with open('ml/helpers/id2label_group.json', 'r') as json_file:
        id2label = json.load(json_file)

    tokens = group_tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        outputs = group_model(**tokens)

    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

    predicted_class_idx = torch.argmax(probs[0]).item()

    return id2label[str(predicted_class_idx)]


def predict_theme(text: str, predicted_group: str):
    text = soft_remove(text)
    with open('ml/helpers/label2id_topic.json', 'r') as json_file:
        label2id = json.load(json_file)

    with open('ml/helpers/id2label_topic.json', 'r') as json_file:
        id2label = json.load(json_file)

    text = predicted_group + text + predicted_group

    tokens = group_tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        outputs = group_model(**tokens)

    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

    predicted_class_idx = torch.argmax(probs[0]).item()

    return id2label[str(predicted_class_idx)]