import trafilatura
import cleaner
from gensim.models import KeyedVectors
from itertools import islice
from tqdm.notebook import tqdm
from re import sub
from sklearn.feature_extraction.text import CountVectorizer
from numpy import array, log
import nltk

url1_keywords = []
url2_keywords = []

def skorla(gelenUrl1, gelenUrl2):

    word_vectors = KeyedVectors.load_word2vec_format('eksiwikimodel', binary=True)
    array_links = []
    array_links.append(gelenUrl1)
    array_links.append(gelenUrl2)
    array_text = []

    for i in array_links:
        html = trafilatura.fetch_url(i)
        text = trafilatura.extract(html)
        text = cleaner.temizle(text)
        array_text.append(text)

    num_lines = sum(1 for line in open("tfidf.txt"))
    with open("tfidf.txt") as file:
        dict_idf = {}
        with tqdm(total=num_lines) as pbar:
            for i, line in tqdm(islice(enumerate(file), 1, None)):
                try:
                    cells = line.split(",")
                    idf = float(sub("[^0-9.]", "", cells[3]))
                    dict_idf[cells[0]] = idf
                except:
                    print("Error on: " + line)
                finally:
                    pbar.update(1)

    vectorizer = CountVectorizer()
    tf = vectorizer.fit_transform([x.lower() for x in array_text])
    tf = tf.toarray()
    tf = log(tf + 1)

    tfidf = tf.copy()
    words = array(vectorizer.get_feature_names())
    for k in tqdm(dict_idf.keys()):
        if k in words:
            tfidf[:, words == k] = tfidf[:, words == k] * dict_idf[k]
        pbar.update(1)

    for j in range(tfidf.shape[0]):
        print("Keywords of article", str(j+1), words[tfidf[j, :].argsort()[-10:][::-1]])

    keywords1 = words[tfidf[0, :].argsort()[-10:][::-1]]
    keywords2 = words[tfidf[1, :].argsort()[-10:][::-1]]

    skor = 0
    for i in range(10):
        for j in range(i+1, 10):
            try:
                point = word_vectors.wv.similarity(w1=keywords1[i], w2=keywords2[j])
                #print(keywords1[i] + " " + keywords2[j] + " point=" + str(point))
                skor += point
            except:
                print(keywords1[i] + " " + keywords2[j] + "not in vocab")

    global url1_keywords
    global url2_keywords
    url1_keywords = keywords1
    url2_keywords = keywords2

    url1_text = nltk.word_tokenize(array_text[0])
    url2_text = nltk.word_tokenize(array_text[1])

    for i in range(0, len(url1_keywords)):
        counter = 0
        for j in range(0, len(url1_text)):
            if url1_keywords[i] == url1_text[j]:
                counter += 1
        url1_keywords[i] = url1_keywords[i] + ': ' + str(counter) + ' adet'

    for i in range(0, len(url2_keywords)):
        counter2 = 0
        for j in range(0, len(url2_text)):
            if url2_keywords[i] == url2_text[j]:
                counter2 += 1
        url2_keywords[i] = url2_keywords[i] + ': ' + str(counter2) + ' adet'

    return skor

def ret_url1keys():
    return url1_keywords

def ret_url2keys():
    return url2_keywords