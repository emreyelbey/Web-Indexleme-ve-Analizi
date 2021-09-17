import trafilatura
import cleaner

from itertools import islice
from tqdm.notebook import tqdm
from re import sub
from sklearn.feature_extraction.text import CountVectorizer
from numpy import array, log

def anahtar(gelenUrl):

    array_links = []
    array_links.append(gelenUrl)
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

    keywords = words[tfidf[0, :].argsort()[-10:][::-1]]
    return keywords