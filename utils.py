import re

import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download("stopwords")
nltk.download("wordnet")

STOPOWRDS = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def cleanup(text):
    words = re.sub(r'([^\s\w]|_)+', '', text).replace('\n', '').split(" ")
    words_without_stopwords = [w.lower() for w in words if w not in STOPOWRDS]
    lemmatized = [lemmatizer.lemmatize(w) for w in words_without_stopwords]
    return " ".join(lemmatized)
