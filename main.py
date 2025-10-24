from datetime import date
import base64
import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from db import db
from models import Noticia

load_dotenv()
print("Chave carregada:", os.getenv("API_KEY"))

app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db.init_app(app)

def dia_de_hoje():
    data_crua = date.today()
    data = data_crua.strftime("%d/%m/%Y")
    return data

def clima_hoje():
        url_pura = "http://api.weatherapi.com/v1/current.json"
        chave_api = os.getenv("API_KEY")

        url = f"{url_pura}?key={chave_api}&q=Guarulhos"
        request_api = requests.get(url)
        clima_geral = request_api.json()
        clima_inteiro = int(clima_geral['current']['temp_c'])
        return clima_inteiro

@app.route("/")
def home():
    noticias = Noticia.query.all() #pegando todas as rows do nosso banco
    clima_guarulhos = clima_hoje()
    hoje = dia_de_hoje()
    return render_template("index.html", noticias=noticias, clima=clima_guarulhos, hoje=hoje)
    

@app.route("/admin")
def admin():
    noticias = Noticia.query.all()
    clima_guarulhos = clima_hoje()
    hoje = dia_de_hoje()
    return render_template("admin.html", noticias=noticias, clima=clima_guarulhos, hoje=hoje)

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
    noticia = Noticia.query.get(noticia_id) #selecionando a noticia especifica que a gente escolheu pra excluir
    db.session.delete(noticia)
    db.session.commit()
    return redirect(url_for('admin'))
    


       
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)