import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
import json
from gensim.utils import simple_preprocess

data = pd.read_csv('BBC_News_Train.csv')
dataCopy = data
data.head()
data['Category'].value_counts()
data.Text = data.Text.apply(simple_preprocess, min_len=3)
data.Text.head()
stop_words = set(stopwords.words('english'))


def stemmingandstop(lis):
    lemmatizer = WordNetLemmatizer()
    filtered_lis = [lemmatizer.lemmatize(w) for w in lis if not w in stop_words and len(w) > 2]
    return filtered_lis


data.Text = data.Text.apply(stemmingandstop)
data.Text.head()
type(data.Text)
data.Text = data.Text.apply(' '.join)
data.head()


X = data.Text
y = data.Category


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', SGDClassifier(loss='hinge', penalty='l2',
                           alpha=1e-3, random_state=42,
                           max_iter=5, tol=None)),
])
parameters = {
 'vect__ngram_range': [(1, 1), (1, 2)],
 'tfidf__use_idf': (True, False),
 'clf__alpha': (1e-3, 1e-4),
}
gs_clf = GridSearchCV(text_clf, parameters, cv=5, n_jobs=-1)
gs_clf = gs_clf.fit(X_train, y_train)
gs_value = gs_clf.predict(X_test)
print(accuracy_score(y_test, gs_value))