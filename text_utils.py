from nltk import word_tokenize
from googletrans import Translator


def tokenize(text):
    tokens = word_tokenize(text)
    return " ".join(tokens)


def remove_rows_with_few_elements(df, column_name):
    # Проверяем наличие столбца в DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Столбец '{column_name}' не найден в DataFrame.")

    # Фильтруем строки с количеством элементов в столбце больше 1
    filtered_df = df[df[column_name].apply(lambda x: len(str(x).split())) > 1]

    return filtered_df


def text_translate(text, src, dest):
    try:
        traslator = Translator()
        traslation = traslator.translate(text=text, src=src, dest=dest)
        return traslation.text
    except Exception as e:
        return e


def filter_data_by_group_count(data, column_name, threshold):
    # Получаем количество записей для каждой группы
    group_counts = data[column_name].value_counts()
    # Получаем список групп, где количество записей меньше или равно порогу
    groups_to_keep = group_counts[group_counts <= threshold].index
    # Фильтруем и возвращаем DataFrame
    filtered_data = data[data[column_name].isin(groups_to_keep)]

    return filtered_data
