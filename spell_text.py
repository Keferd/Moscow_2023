from transformers import AutoModelForSeq2SeqLM, T5TokenizerFast
import torch

import preprocessing

MODEL_NAME = 'UrukHan/t5-russian-spell'
MAX_INPUT = 256

# Загрузка модели и токенизатора
tokenizer = T5TokenizerFast.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def spell_txt(input_sequences):
    task_prefix = "Spell correct: "
    if type(input_sequences) != list: input_sequences = [input_sequences]
    encoded = tokenizer(
        [task_prefix + sequence for sequence in input_sequences],
        padding="longest",
        max_length=MAX_INPUT,
        truncation=True,
        return_tensors="pt",
    )

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    encoded.to(device)

    predicts = model.generate(**encoded)
    new_text = tokenizer.batch_decode(predicts, skip_special_tokens=True)
    new_text = preprocessing.remove_duplicate_puntcs(new_text[0])
    return new_text


text = """Когда будет расчищена улица Радищева от Артёма до Сакко и Ванцетти.Огромные колеи лёд,вчера машины буксовал,не дорога а одно название!!???"""

print(spell_txt(text))
