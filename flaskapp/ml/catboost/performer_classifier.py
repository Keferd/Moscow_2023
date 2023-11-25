import joblib
from catboost import CatBoostClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

class_dict = {'Лысьвенский городской округ': 1, 'Город Пермь': 2, 'Губахинский городской округ': 3, 'Министерство здравоохранения': 4, 'Бардымский муниципальный округ Пермского края': 5, 'Александровский муниципальный округ Пермского края': 6, 'Министерство социального развития ПК': 7,
              'ИГЖН ПК': 8, 'АО ПРО ТКО': 9, 'Министерство образования': 10}

def performer_classifier(group, topic):
    text = group + " " + topic

    model_path = 'D:\Projects\Hackathons\Цифровой прорыв - Москва(Международный) 2023\Web\Moscow_2023/flaskapp\ml\catboost\my_catboost_model_2'
    catboost_model = CatBoostClassifier()
    catboost_model.load_model(model_path)

    vectorizer_path = 'vectorizer.pkl'
    vectorizer = joblib.load(vectorizer_path)
    text_vectorized = vectorizer.transform(text)
    prediction = catboost_model.predict(text_vectorized)

    for key, value in class_dict.items():
        if value == prediction:
            prediction = key
    return prediction