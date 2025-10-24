import sqlite3
import base64
from flask import Flask, render_template, request, redirect
from db import db
from models import Noticia


app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db.init_app(app)

@app.route("/")
def home():
    noticias = Noticia.query.all() #pegando todas as rows do nosso banco
    for noticia in noticias:
        print(f"Título: {noticia.titulo}")
    return render_template("index.html", noticias=noticias)
    

@app.route("/admin")
def admin():
    noticias = Noticia.query.all()
    return render_template("admin.html", noticias=noticias)

@app.route("/nova_noticia", methods=['GET', 'POST'])
def nova_noticia():
    if request.method == 'GET':
        return render_template("nova-noticia.html")
    else:
        titulo = request.form['tituloForm']
        capa = request.files['imgForm'].read()
        link = request.form['urlForm']

        noticia = Noticia(titulo=titulo, capa=capa, link=link)
        db.session.add(noticia)
        db.session.commit()
        print("Dados inseridos no banco!")
        return redirect('admin')

@app.template_filter('b64encode') #rota pra decodar arquivos binários em imagens
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

@app.route("/delete", methods=['POST'])
def deletar_noticia():
    noticia_id = request.form['id']
    


       
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)