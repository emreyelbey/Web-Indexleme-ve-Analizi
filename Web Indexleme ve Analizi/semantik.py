import trafilatura
import cleaner

from gensim.models import KeyedVectors
import anahtar
import nltk

def analizet(gelenUrl):
    word_vectors = KeyedVectors.load_word2vec_format('eksiwikimodel', binary=True)

    html = trafilatura.fetch_url(gelenUrl)
    text = trafilatura.extract(html)
    text = cleaner.temizle(text)
    words = nltk.word_tokenize(text)
    keywords = anahtar.anahtar(gelenUrl)
    semantikler = keywords

    for i in range(0, len(keywords)):
        for j in range(0, len(words)):
            try:
                if 0.5 < word_vectors.wv.similarity(w1=str(words[j]), w2=str(keywords[i])) < 1:
                    semantikler[i] = semantikler[i] + ' - ' + words[j]
            except:
                print("not in voc")

    return semantikler