from itertools import islice
from tqdm.notebook import tqdm
from re import sub
from sklearn.feature_extraction.text import CountVectorizer
from numpy import array, log
import numpy as np
import nltk
import agac

from operator import itemgetter
import trafilatura
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
from urllib import request
import re
from gensim.models import KeyedVectors

word_vectors = KeyedVectors.load_word2vec_format('eksiwikimodel', binary=True)

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

katman2links = []
katman3links = []
tumlinks = []
array_text = []
array_text1 = []
array_text2 = []
array_text3 = []


# called by each thread
def get_url(katman1link):
    k = 0
    try:
        html_page = request.urlopen(katman1link).read()
        soup = BeautifulSoup(html_page)

        try:
            text = trafilatura.extract(html_page)
            regex = re.compile('[^a-zA-Z öçşiğüÖÇŞİĞÜı\n\r\t\b]')
            text = regex.sub('', text)
            text = " ".join(text.split())
            text = text.replace("İ", "i")
            text = text.lower()
            array_text.append([katman1link, text])
            # print(katman1link)

        except:
            array_text.append("text alinamadi")

        for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
            katman2links.append(link.get('href'))

            try:
                html = request.urlopen(link.get('href')).read()
                text = trafilatura.extract(html)
                regex = re.compile('[^a-zA-Z öçşiğüÖÇŞİĞÜı\n\r\t\b]')
                text = regex.sub('', text)
                text = " ".join(text.split())
                text = text.replace("İ", "i")
                text = text.lower()
                array_text.append([link.get('href'), text])

            except:
                array_text.append("text alinamadi")
            k += 1
            if k == 2:
                break
    except:
        print("error")


def get_url2(katman2link):
    k = 0
    try:
        html_page = request.urlopen(katman2link).read()
        soup = BeautifulSoup(html_page)

        for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
            katman3links.append(link.get('href'))

            try:
                html = request.urlopen(link.get('href')).read()
                text = trafilatura.extract(html)
                regex = re.compile('[^a-zA-Z öçşiğüÖÇŞİĞÜı\n\r\t\b]')
                text = regex.sub('', text)
                text = " ".join(text.split())
                text = text.replace("İ", "i")
                text = text.lower()
                array_text.append([link.get('href'), text])

            except:
                array_text.append("text alinamadi")
            k += 1
            if k == 2:
                break
    except:
        print("exceppppttt")


def indexle(gelenUrl, gelenUrlKumesi):
    gelenUrlKumesi = " ".join(gelenUrlKumesi.split())
    print("00000000000000000000000000000000000000000000000")
    # print(gelenUrlKumesi)
    katman1links = gelenUrlKumesi.split()
    # print(katman1links)

    html_page = request.urlopen(gelenUrl).read()
    text = trafilatura.extract(html_page)
    regex = re.compile('[^a-zA-Z öçşiğüÖÇŞİĞÜı\n\r\t\b]')
    text = regex.sub('', text)
    text = " ".join(text.split())
    text = text.replace("İ", "i")
    text = text.lower()
    array_text.append([gelenUrl, text])

    pool = ThreadPool(16)
    # pool.map(get_url, gelenUrl)
    pool.map(get_url, katman1links)
    pool.map(get_url2, katman2links)
    tumlinks = katman1links + katman2links + katman3links

    pool.close()
    pool.join()
    #################################################

    vectorizer = CountVectorizer()
    tf = vectorizer.fit_transform([row[1] for row in array_text])
    tf = tf.toarray()
    tf = log(tf + 1)

    tfidf = tf.copy()
    words = array(vectorizer.get_feature_names())
    for k in tqdm(dict_idf.keys()):
        if k in words:
            tfidf[:, words == k] = tfidf[:, words == k] * dict_idf[k]
        pbar.update(1)

    wordlist = []
    for k in range(0, len(array_text)):
        wordlist.append(words[tfidf[k, :].argsort()[-10:][::-1]])

    newwords = []
    for words in wordlist:
        save = []
        for word in words:
            save.append(word)
        newwords.append(save)
        del save

    totalpoint = 0
    listofindexing = []
    katsayi = 1
    for k in range(1, len(array_text)):
        if k < 1 + len(katman1links):
            katsayi = 20
        elif k > 1 + len(katman1links) and k < 1 + len(katman1links) + len(katman2links):
            katsayi = 7
        else:
            katsayi = 3
        for i in range(10):
            for j in range(i + 1, 10):
                try:
                    point = word_vectors.wv.similarity(w1=wordlist[0][i], w2=wordlist[k][j])
                    # print(wordlist[0][i] + " " + wordlist[k][j] + " point=" + str(point))
                    totalpoint += (katsayi * point)
                except:
                    pass

        for i in range(0, len(array_text[k][1])):
            text_kelimeler = nltk.word_tokenize(array_text[k][1])

        for i in range(0, len(newwords[k])):
            counter = 0
            for j in range(0, len(text_kelimeler)):
                if newwords[k][i] == text_kelimeler[j]:
                    counter += 1
            newwords[k][i] = newwords[k][i] + ': ' + str(counter) + ' adet'

        listofindexing.append([array_text[k][0], totalpoint, newwords[k]])
        # print(listofindexing[k-1])
        totalpoint = 0

    sortedlist = sorted(listofindexing, key=itemgetter(1), reverse=True)
    # print(listofindexing)
    print(sortedlist)

    agac.indexle(gelenUrl, gelenUrlKumesi)
    return sortedlist