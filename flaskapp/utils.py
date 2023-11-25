import pandas as pd

from flaskapp.ml.inference import predict_group, predict_theme
from preprocessing import soft_remove
from spell_and_summarization import spell_txt, summarization_txt
from ner import extract_addresses


def add_group_column(df):
    df['group'] = df['text'].copy().apply(lambda x: predict_group(soft_remove(x)))
    return df


def add_topic_column(df):
    df['topic'] = df.apply(lambda row: predict_theme(soft_remove(row['text']), row['group']), axis=1)
    return df


def add_spell_text(df):
    df['spell'] = df['text'].copy().apply(lambda x: spell_txt(soft_remove(x)))
    return df


def add_summarization_text(df):
    df['summarization'] = df['text'].copy().apply(lambda x: summarization_txt(soft_remove(x)))
    return df


def add_loc(df):
    df['loc'] = df['spell'].copy().apply(lambda x: extract_addresses(x))
    return df


def subbmit(df):
    df = add_group_column(df)
    df = add_topic_column(df)
    df = df.drop(columns="text")
    df.columns = ["id", "Группа тем", "Тема"]
    df.to_csv('submission.csv', sep=';', index=False, encoding='utf-8')
    return df


def get_frontend_table(df):
    df = add_group_column(df)
    df = add_topic_column(df)
    df = add_spell_text(df)
    df = add_summarization_text(df)
    df = add_loc(df)
    return df

# test = pd.read_csv("test.csv", encoding="UTF-8", sep=";")
# test.columns = ["id", "text"]
#
# subbmit(test)

