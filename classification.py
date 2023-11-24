import pandas as pd
from joblib import dump
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier

import preprocessing
import text_utils

train = pd.read_csv("train_dataset_train.csv", encoding="UTF-8", sep=";")
train.columns = ['performer', 'group', 'text', 'topic']

train = text_utils.remove_rows_with_few_elements(train, 'text')
train['text'] = train['text'].apply(preprocessing.remove_all_trash)
train['text'] = train['text'].apply(text_utils.tokenize)

X_train, X_test, y_train, y_test = train_test_split(train['text'], train['group'], test_size=0.2, random_state=42,
                                                    stratify=train['group'])


# -----Logistic Regression-----
print('Logistic Regression')
logreg = Pipeline([('vect', CountVectorizer()),
                   ('tfidf', TfidfTransformer()),
                   ('clf', LogisticRegression(n_jobs=1, C=1e5, max_iter=1000)),
                   ])
logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)
print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred, target_names=train['group'].unique(), zero_division=0))
dump(logreg, 'models/logistic_regression_classifier.joblib')

# -----Passive Aggressive Classifier-----
print('Passive Aggressive Classifier')
pac = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', PassiveAggressiveClassifier(max_iter=1000, random_state=42, tol=None)),
                ])
pac.fit(X_train, y_train)
y_pred = pac.predict(X_test)
print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred, target_names=train['group'].unique(), zero_division=0))
dump(pac, 'models/passive_aggressive_classifier.joblib')


# -----Support Vector Classifier-----
print('Support Vector Classifier')
svc = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', SVC(kernel='linear', C=1.0, random_state=42, max_iter=1000)),
                ])
svc.fit(X_train, y_train)
y_pred = svc.predict(X_test)
print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred, target_names=train['group'].unique(), zero_division=0))


# -----Voting Classifier-----
print('Voting Classifier')
estimators = [('lr', LogisticRegression(n_jobs=1, C=1e5, max_iter=1000)),
              ('sv', SVC(kernel='linear', C=1.0, random_state=42, max_iter=1000)),
              ('pac', PassiveAggressiveClassifier(max_iter=1000, random_state=42, tol=None))]

voting = Pipeline([('vect', CountVectorizer()),
                   ('tfidf', TfidfTransformer()),
                   ('clf', VotingClassifier(estimators=estimators, voting='hard')),
                   ])
voting.fit(X_train, y_train)
y_pred = voting.predict(X_test)
print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred, target_names=train['group'].unique(), zero_division=0))
