#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC

df_orig = pd.read_csv('news_topics_music.csv')
df_orig.head()

#df_sru = pd.read_csv('news_topics_sru.csv')
#df_sru.head()

df = pd.concat([df_orig])
df.shape
df = df.drop([], axis=1)
df.head()

topics = ['music', 'politics', 'business', 'culture', 'science',
          'sports', 'crime', 'disasters', 'environment', 'health',
          'education', 'religion', 'lifestyle', 'other']

df['sum_0'] = (df[topics] == 0).sum(axis=1)
df['sum_1'] = (df[topics] == 1).sum(axis=1)
df['sum_2'] = (df[topics] == 2).sum(axis=1)

df.head(10)

non_unique = df.loc[df['sum_1'] != 1]
non_unique.shape

df.shape[0]
counts = [df.shape[0] - df[t].value_counts()[0] for t in topics]
print(topics, counts)

df[topics].as_matrix()
df[topics] = df[topics].replace(to_replace=2, value=1)
df[topics].as_matrix()

topics = ['music', 'politics', 'business', 'culture', 'science', 'sports']
X_train, X_test, y_train, y_test = train_test_split(df['ocr'], df[topics].as_matrix(), random_state=0)
X_train.shape, y_train.shape
X_test.shape, y_test.shape

count_vect = TfidfVectorizer(min_df=6, max_df=0.9, ngram_range=(2,5), analyzer='char_wb', max_features=10000)
X_train_counts = count_vect.fit_transform(X_train)
X_test_counts = count_vect.transform(X_test)

len(count_vect.vocabulary_.keys())
joblib.dump(count_vect, 'news_topics_nl_vct.pkl')
clf = OneVsRestClassifier(SVC(probability=True, kernel='linear', class_weight='balanced', C=1.0, verbose=True))
clf.fit(X_train_counts, y_train)

joblib.dump(clf, 'news_topics_nl_clf.pkl')
pred = clf.predict(X_test_counts)
roc_auc_score(y_test, pred)
accuracy_score(y_test, pred)
print('average precision', precision_score(y_test, pred, average='macro'))
print('average recall', recall_score(y_test, pred, average='macro'))
print('average f1', f1_score(y_test, pred, average='macro'))

scores = {}
scores['precision'] = precision_score(y_test, pred, average=None)
scores['recall'] = recall_score(y_test, pred, average=None)
scores['f1'] = f1_score(y_test, pred, average=None)
pd.DataFrame(data=scores, index=topics)
article = '''Minister Romme en partijgenoot Lieftinck van het CDA verlieten gisteren het Binnenhof
        om met de priester in de kerk te gaan praten over de zin en onzin van religieuze geboortebeperking.
        Computer op komst.'''
article_counts = count_vect.transform([article])
clf.predict_proba(article_counts)
