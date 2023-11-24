from transformers import AutoModelForSeq2SeqLM, T5TokenizerFast
import torch

import preprocessing

MODEL_SPELL = 'UrukHan/t5-russian-spell'
MODEL_SUM = 'UrukHan/t5-russian-summarization'
MAX_INPUT = 256

# Загрузка модели и токенизатора
spell_tokenizer = T5TokenizerFast.from_pretrained(MODEL_SPELL)
spell_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_SPELL)

sum_tokenizer = T5TokenizerFast.from_pretrained(MODEL_SUM)
sum_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_SUM)

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
spell_model.to(device)
sum_model.to(device)


def spell_txt(input_sequences):
    task_prefix = "Spell correct: "
    if type(input_sequences) != list: input_sequences = [input_sequences]
    encoded = spell_tokenizer(
        [task_prefix + sequence for sequence in input_sequences],
        padding="longest",
        max_length=MAX_INPUT,
        truncation=True,
        return_tensors="pt",
    )

    encoded.to(device)
    predicts = spell_model.generate(**encoded)
    new_text = spell_tokenizer.batch_decode(predicts, skip_special_tokens=True)
    new_text = preprocessing.remove_duplicate_puntcs(new_text[0])
    return new_text


def summarization_txt(input_sequences):
    task_prefix = "Summarization correct: "
    if type(input_sequences) != list: input_sequences = [input_sequences]
    encoded = spell_tokenizer(
        [task_prefix + sequence for sequence in input_sequences],
        padding="longest",
        max_length=MAX_INPUT,
        truncation=True,
        return_tensors="pt",
    )

    encoded.to(device)
    predicts = sum_model.generate(**encoded)
    new_text = sum_tokenizer.batch_decode(predicts, skip_special_tokens=True)
    new_text = preprocessing.remove_duplicate_puntcs(new_text[0])
    return new_text
