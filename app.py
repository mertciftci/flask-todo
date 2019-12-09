from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
app = Flask(__name__)

app.secret_key = "Çok gizli bir key"

#veri tabanı bağlantsı
client = MongoClient(
    "mongodb+srv://egitim:<egitim48>@cluster0-xolkq.mongodb.net/test?retryWrites=true&w=majority"
)
#tododb veritabanı adı todos kolleksiyon ismi
db = client.tododb.todos
#artık db. ile veri tabanında her şeyi yapabilirim


@app.route('/')
def index():
    #veri tabanına kayıtları çek bir listeye al
    yapilacaklar = []
    for yap in db.find():
        yapilacaklar.append({
            "_id": str(yap.get("_id")),
            "isim": yap.get("isim"),
            "durum": yap.get("durum")
        })

    #index.html'e bu listeyi yollayın

    return render_template('index.html', yapilacaklar=yapilacaklar)


@app.route('/guncelle/<id>')
def guncelle(id):
    #gelen id değeri ile kaydı bulalım
    #durum değeri true ise false false ise true yapalım
    yap = db.find({'_id': ObjectId(id)})
    durum = not yap.get('durum')
    #kaydı güncelle
    db.find_one_and_update({'_id': ObjectId(id)}, {'$set': {'durum': durum}})
    #ana sayfaya yönlendir
    return redirect('/')


@app.route('/sil/<id>')
def sil(id):
    db.find_one_and_delete({'_id': ObjectId(id)})
    return redirect('/')


@app.route('/ekle', methods=['POST'])
def ekle():
    isim = request.form.get['isim']
    db.insert_one({'isim': isim, 'durum': 'False'})
    #ana sayfaya yönlendirir.
    return redirect('/')


@app.errorhandler(404)
def hataliurl():
    return redirect('/')


@app.route('/kimiz')
def kimiz():
    return render_template('kimiz.html')


@app.route('/user/<isim>')
def user(isim):
    return render_template('user.html', isim=isim)


if __name__ == '__main__':
    app.run(debug=True)
