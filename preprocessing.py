import nltk
from nltk.corpus import stopwords
import re

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

CUSTOM_STOPWORDS = ['здравствуйте', 'и', 'в', 'во', 'что', 'он', 'на', 'я', 'нас',
                    'привет', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так',
                    'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы',
                    'за', 'бы', 'по', 'только', 'ее', 'мне', 'было',
                    'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему',
                    'теперь', 'когда', 'даже', 'ну', 'вдруг', 'ли',
                    'если', 'уже', 'или', 'быть', 'был', 'него',
                    'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь',
                    'там', 'потом', 'себя', 'ничего', 'ей', 'может', 'они',
                    'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя',
                    'их', 'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего',
                    'раз', 'тоже', 'себе', 'под', 'будет', 'ж', 'тогда', 'кто',
                    'этот', 'того', 'потому', 'этого', 'какой', 'совсем',
                    'ним', 'здесь', 'этом', 'один', 'почти', 'мой', 'тем',
                    'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем', 'всех',
                    'можно', 'при', 'наконец', 'два', 'об', 'другой',
                    'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти',
                    'про', 'всего', 'них', 'какая', 'много', 'разве', 'три', 'эту',
                    'моя', 'впрочем', 'хорошо', 'свою', 'этой', 'перед', 'иногда',
                    'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более',
                    'всегда', 'конечно', 'всю', 'между']


def remove_vk_specials(text: str) -> str:
    pattern = re.compile(r'\[(club|id)\d+\|[^\]]+\]')
    return re.sub(pattern, '', text)


def remove_emoji(text):
    pattern_emoji = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    return pattern_emoji.sub('', text)


def remove_urls(text: str) -> str:
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    text = re.sub(pattern, '', text)
    return text


def remove_emails(text):
    email_pattern = re.compile(r'\S+@\S+')
    return email_pattern.sub('', text)


def remove_html_tags(text):
    pattern = re.compile(r'<[^>]+>')
    text = re.sub(pattern, '', text)
    return text


def remove_numbers(text):
    pattern = re.compile(r'(?:(?:\d+,?)+(?:\.?\d+)?)')
    text = re.sub(pattern, '', text)
    return text


def remove_extra_spaces(text):
    return ' '.join(text.split())


def remove_special_characters(text):
    special_characters = "@#$%^&*+<>_'"
    return ''.join(char for char in text if char not in special_characters)


def remove_all_puncts(text):
    return re.sub(r'[^\w\s]', ' ', text)


def convert_to_lowercase(text):
    return text.lower()


def remove_stopwords(text, custom_stopwords):
    stopword_list = stopwords.words("russian")
    if custom_stopwords:
        stopword_list.extend(CUSTOM_STOPWORDS)
    words = text.split()
    filtered_words = [word for word in words if word not in stopword_list]
    return ' '.join(filtered_words)


def remove_all_trash(text, punct=False, stopword=False, custom_stopwords=True):
    text = remove_emoji(text)
    text = remove_vk_specials(text)
    text = remove_emails(text)
    text = remove_html_tags(text)
    text = remove_urls(text)
    text = remove_numbers(text)
    if punct:
        text = remove_special_characters(text)
    else:
        text = remove_all_puncts(text)
    text = convert_to_lowercase(text)
    text = remove_extra_spaces(text)
    if not stopword:
        text = remove_stopwords(text, custom_stopwords)
    return text


def soft_remove(text):
    text = remove_emoji(text)
    text = remove_vk_specials(text)
    text = remove_emails(text)
    text = remove_html_tags(text)
    text = remove_urls(text)
    text = remove_special_characters(text)
    text = remove_extra_spaces(text)
    return text
