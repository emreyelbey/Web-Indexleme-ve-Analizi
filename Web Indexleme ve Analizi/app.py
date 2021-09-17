import kelimefrekanslari, benzerlikskorlama, anahtar, webindex, semantik, agac
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")    

@app.route("/kelimefrekansi", methods = ["GET", "POST"])
def kelimefrekansi():
    if request.method == "POST":
        gelenUrl = request.form.get("gelen_url")
        frekans = kelimefrekanslari.hesapla(gelenUrl)
        toplam_ks = kelimefrekanslari.ret_toplam_ks(frekans)
        farkli_ks = kelimefrekanslari.ret_farkli_ks(frekans)
        return render_template("kelimefrekansi.html", frekans=frekans, toplam_ks=toplam_ks, farkli_ks=farkli_ks)
    else:
        return redirect(url_for("home"))

@app.route("/anahtarkelime", methods = ["GET", "POST"])
def anahtarkelime():
    if request.method == "POST":
        gelenUrl = request.form.get("gelen_url")
        keywords = anahtar.anahtar(gelenUrl)
        return render_template("anahtarkelime.html", keywords=keywords)
    else:
        return redirect(url_for("home"))

@app.route("/benzerlikskoru", methods = ["GET", "POST"])
def benzerlikskoru():
    if request.method == "POST":
        gelenUrl1 = request.form.get("gelen_url1")
        gelenUrl2 = request.form.get("gelen_url2")
        skor = benzerlikskorlama.skorla(gelenUrl1, gelenUrl2)
        url1Keys = benzerlikskorlama.ret_url1keys()
        url2Keys = benzerlikskorlama.ret_url2keys()
        return render_template("benzerlikskoru.html", skor=skor, url1Keys=url1Keys, url2Keys=url2Keys)
    else:
        return redirect(url_for("home"))

@app.route("/siteindexleme", methods = ["GET", "POST"])
def siteindexleme():
    if request.method == "POST":
        gelenUrl = request.form.get("gelen_url")
        gelenUrlKumesi = request.form.get("gelen_url_kumesi")
        tree = webindex.indexle(gelenUrl, gelenUrlKumesi)
        return render_template("siteindexleme.html", tree=tree)
    else:
        return redirect(url_for("home"))

@app.route("/semantik", methods = ["GET", "POST"])
def semantikanaliz():
    if request.method == "POST":
        gelenUrl = request.form.get("gelen_url")
        semantikler = semantik.analizet(gelenUrl)
        return render_template("semantik.html", semantikler=semantikler)
    else:
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)