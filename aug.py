import pandas as pd
import text_utils
import preprocessing


def process_row(row):
    duplicate_row = row.copy()
    duplicate_row['text'] = preprocessing.soft_remove(duplicate_row['text'])
    if len(duplicate_row['text']) < 2:
        return None
    duplicate_row['text'] = text_utils.text_translate(duplicate_row['text'], "ru", "en")
    return duplicate_row


def aug_csv(df):
    # Применяем функцию process_row ко всем строкам
    new_data = df.apply(process_row, axis=1).dropna()  # dropna, чтобы удалить строки с пустыми значениями

    new_data.to_csv("new_data.csv", encoding='UTF-8', sep=';', index=False)


data = pd.read_csv("train_dataset_train.csv", encoding="UTF-8", sep=";")
data.columns = ['performer', 'group', 'text', 'topic']

data = text_utils.filter_data_by_group_count(data, 'group', 25)
aug_csv(data)
