from nltk import word_tokenize


def remove_rows_with_few_elements(df, column_name):
    """
    Удаляет строки из DataFrame, если количество элементов в указанном столбце меньше или равно 1.

    Parameters:
    - df: pandas.DataFrame
        Исходный DataFrame.
    - column_name: str
        Имя столбца, по которому проверяется количество элементов.

    Returns:
    - pandas.DataFrame
        DataFrame с удаленными строками.
    """
    # Проверяем наличие столбца в DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Столбец '{column_name}' не найден в DataFrame.")

    # Фильтруем строки с количеством элементов в столбце больше 1
    filtered_df = df[df[column_name].apply(lambda x: len(str(x).split())) > 1]

    return filtered_df


def tokenize(text):
    tokens = word_tokenize(text)
    return " ".join(tokens)
