def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import normalize
from utils import pairs
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download("wordnet")
nltk.download("omw-1.4")

def dummy(doc):
    return doc

def do_svm(pair):

    lemmatizer = WordNetLemmatizer()

    stop_words = sorted(list(set(stopwords.words('english'))))

    word_vectorizer = CountVectorizer(tokenizer=dummy, preprocessor=dummy)
    no_stop_vectorizer = CountVectorizer(tokenizer=dummy, preprocessor=dummy)
    pos_vectorizer = CountVectorizer(tokenizer=dummy, preprocessor=dummy)
    lemma_vectorizer = CountVectorizer(tokenizer=dummy, preprocessor=dummy)
    ngram_vectorizer = CountVectorizer(analyzer="char", ngram_range=(1, 5))

    folder = "_".join(pair)

    with open("pairs/" + folder + "/" + pair[0] + ".json", "r") as file:
        first_texts = json.load(file)

    with open("pairs/" + folder + "/" + pair[1] + ".json", "r") as file:
        second_texts = json.load(file)

    len_first = len(first_texts.keys())
    len_second = len(second_texts.keys())
    if len_first > len_second:
        first_texts = dict(list(first_texts.items())[:-(len_first-len_second)])
    elif len_second > len_first:
        second_texts = dict(list(second_texts.items())[:-(len_second-len_first)])

    first_tokenized_train_texts = []
    second_tokenized_train_texts = []
    first_tokenized_test_texts = []
    second_tokenized_test_texts = []
    first_string_train_list = []
    second_string_train_list = []
    first_string_test_list = []
    second_string_test_list = []

    for key in first_texts.keys():
        first_tokenized_train_texts += first_texts[key][2:]
        first_tokenized_test_texts += first_texts[key][:2]
        first_string_train_list += map(lambda s: " ".join(s), first_texts[key][2:])
        first_string_test_list += map(lambda s: " ".join(s), first_texts[key][:2])

    for key in second_texts.keys():
        second_tokenized_train_texts += second_texts[key][2:]
        second_tokenized_test_texts += second_texts[key][:2]
        second_string_train_list += map(lambda s: " ".join(s), second_texts[key][2:])
        second_string_test_list += map(lambda s: " ".join(s), second_texts[key][:2])

    def extract_features(tokenized_texts, string_list, do_fit=True):
        if do_fit:
            texts_no_stops = list(map(lambda t: filter(lambda w: w in stop_words, t), tokenized_texts))
            bow_no_stops = no_stop_vectorizer.fit_transform(texts_no_stops).toarray()
            bow = word_vectorizer.fit_transform(tokenized_texts).toarray()
            ngrams = ngram_vectorizer.fit_transform(string_list).toarray()
            pos = pos_vectorizer.fit_transform(map(lambda t: map(lambda p: p[1], t), map(pos_tag, tokenized_texts))).toarray()
            lemma = lemma_vectorizer.fit_transform(map(lambda l: map(lemmatizer.lemmatize, l), tokenized_texts)).toarray()
        else:
            bow = word_vectorizer.transform(tokenized_texts).toarray()
            bow_no_stops = no_stop_vectorizer.transform(tokenized_texts).toarray()
            ngrams = ngram_vectorizer.transform(string_list).toarray()
            pos = pos_vectorizer.transform(map(lambda t: map(lambda p: p[1], t), map(pos_tag, tokenized_texts))).toarray()
            lemma = lemma_vectorizer.transform(map(lambda l: map(lemmatizer.lemmatize, l), tokenized_texts)).toarray()
        features = []

        for i in range(bow.shape[0]):
            features.append(normalize([list(bow[i]) + list(bow_no_stops[i]) + list(ngrams[i]) + list(pos[i]) + list(lemma[i])])[0])

        return features

    first_train_features = extract_features(first_tokenized_train_texts, first_string_train_list)
    first_test_features = extract_features(first_tokenized_test_texts, first_string_test_list, do_fit=False)
    second_train_features = extract_features(second_tokenized_train_texts, second_string_train_list)
    second_test_features = extract_features(second_tokenized_test_texts, second_string_test_list, do_fit=False)
    onetwo_train_features = extract_features(first_tokenized_train_texts, first_string_train_list)
    onetwo_test_features = extract_features(second_tokenized_train_texts, second_string_train_list, do_fit=False)
    twoone_train_features = extract_features(second_tokenized_train_texts, second_string_train_list)
    twoone_test_features = extract_features(first_tokenized_train_texts, first_string_train_list, do_fit=False)

    first_train_labels = list(np.repeat(list(first_texts.keys()), 23))
    first_correct_test_labels = list(np.repeat(list(first_texts.keys()), 2))
    onetwo_labels = first_train_labels
    second_train_labels = list(np.repeat(list(second_texts.keys()), 23))
    second_correct_test_labels = list(np.repeat(list(second_texts.keys()), 2))
    twoone_labels = second_train_labels

    print("Users: " + str(len(first_texts.keys())))

    first_clf = SVC(kernel="linear", C = 1.0)
    first_clf.fit(first_train_features, first_train_labels)

    second_clf = SVC(kernel="linear", C = 1.0)
    second_clf.fit(second_train_features, second_train_labels)

    onetwo_clf = SVC(kernel="linear", C = 1.0)
    onetwo_clf.fit(onetwo_train_features, onetwo_labels)

    twoone_clf = SVC(kernel="linear", C = 1.0)
    twoone_clf.fit(twoone_train_features, twoone_labels)

    print(str(100 * len(list(filter(lambda p: p[0] == p[1], zip(first_correct_test_labels, first_clf.predict(first_test_features))))) / len(first_correct_test_labels)) + " %")

    print(str(100 * len(list(filter(lambda p: p[0] == p[1], zip(second_correct_test_labels, second_clf.predict(second_test_features))))) / len(second_correct_test_labels)) + " %")

    print(str(100 * len(list(filter(lambda p: p[0] == p[1], zip(twoone_labels, onetwo_clf.predict(onetwo_test_features))))) / len(twoone_labels)) + " %")

    print(str(100 * len(list(filter(lambda p: p[0] == p[1], zip(onetwo_labels, twoone_clf.predict(twoone_test_features))))) / len(onetwo_labels)) + " %")
           

if __name__ == "__main__":
    for pair in pairs:
        print("Pair = " + str(pair))
        do_svm(pair)