import re
def temizle(s1):
    s1 = str(s1)
    regex = re.compile('[^a-zA-Z öçşiğüÖÇŞİĞÜı\n\r\t\b]')
    s1 = regex.sub('', s1)

    s1 = " ".join(s1.split())
    s1 = s1.replace("İ", "i")
    s1 = s1.lower()
    return s1
