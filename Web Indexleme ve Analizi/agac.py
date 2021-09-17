import trafilatura
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
from urllib import request
import re

katman1links = []
katman2links = []
katman3links = []

def get_url(katman1links):
    for katman1link in katman1links:
        k = 0
        katman2save = []
        try:
            html_page = request.urlopen(katman1link).read()
            soup = BeautifulSoup(html_page)

            for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
                katman2save.append(link.get('href'))
                k += 1
                if (k % 5 == 0):
                    break
        except:
            print("error")

        katman2links.append(katman2save)
        del katman2save

def get_url2(katman2linklers):
    for katman2linkler in katman2linklers:

        k = 0
        katman3save = []
        for katman2link in katman2linkler:
            saveci = []
            try:
                html_page = request.urlopen(katman2link).read()
                soup = BeautifulSoup(html_page)

                for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
                    sonlink = link.get('href')
                    saveci.append(sonlink)

                    k += 1
                    if (k % 5 == 0):
                        break

            except:
                print("error")
            katman3save.append(saveci)
            del saveci
        katman3links.append(katman3save)
        del katman3save

def indexle(gelenUrl, gelenUrlKumesi):

    gelenUrlKumesi = " ".join(gelenUrlKumesi.split())
    global katman1links
    global katman2links
    global katman3links
    katman1links = gelenUrlKumesi.split()

    get_url(katman1links)
    get_url2(katman2links)

    for i in range(0, len(katman1links)):
        print(katman1links[i])
        for j in range(0, len(katman2links[i])):
            print('         ', end="")
            print(katman2links[i][j])
            for k in range(0, len(katman3links[i][j])):
                print('                  ', end="")
                print(katman3links[i][j][k])

    text = 31
    return text

def ret_katman1():
    return katman1links

def ret_katman2():
    return katman2links

def ret_katman3():
    return katman3links