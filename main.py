import base64
import os
import requests
import random
from dotenv import load_dotenv
from datetime import date
from flask import Flask, render_template, request, redirect, url_for
from db import db
from models import Noticia

load_dotenv()

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

def gerador_de_frase():      
    frases = [
        "A persistência realiza o impossível.",
        "Grandes conquistas começam com pequenos passos.",
        "Acredite no processo.",
        "O sucesso é a soma de pequenos esforços repetidos diariamente.",
        "Nada floresce sem dedicação.",
        "Sonhar é o primeiro passo para realizar.",
        "Faça o seu melhor hoje, o amanhã depende disso.",
        "Cada desafio é uma oportunidade disfarçada.",
        "A disciplina supera a motivação.",
        "O progresso é mais importante que a perfeição.",
        "Você é mais capaz do que imagina.",
        "Um passo de cada vez ainda é progresso.",
        "A atitude é o que transforma intenção em ação.",
        "Seja constante, não apenas entusiasmado.",
        "Grandes mudanças exigem coragem.",
        "A jornada vale tanto quanto o destino.",
        "Trabalhe em silêncio e deixe o resultado fazer barulho.",
        "Nada muda se você não mudar.",
        "Tempo e esforço sempre trazem frutos.",
        "A mente é o que diferencia os fortes dos fracos.",
        "A sorte favorece quem está preparado.",
        "Você não precisa ser o melhor, apenas melhor que ontem.",
        "Mesmo devagar, vá em frente.",
        "Não espere oportunidades, crie-as.",
        "Faça o que é certo, não o que é fácil.",
        "A paciência é o segredo de todo sucesso duradouro.",
        "O esforço de hoje é o sucesso de amanhã.",
        "A melhor motivação é ver até onde você já chegou.",
        "A força vem quando você pensa que não tem mais nada e continua mesmo assim.",
        "Acredite: você está no caminho certo.",
        "Erros são provas de que você está tentando.",
        "A cada queda, levante-se mais forte.",
        "Transforme obstáculos em degraus.",
        "Seja sua própria motivação.",
        "Resultados exigem constância.",
        "A melhor maneira de prever o futuro é criá-lo.",
        "Persistir é a arte de continuar quando tudo diz para parar.",
        "O esforço vence o talento quando o talento não se esforça.",
        "Toda conquista começa com a decisão de tentar.",
        "Quem quer, arruma um jeito; quem não quer, arruma uma desculpa.",
        "Você é responsável por sua própria evolução.",
        "Não pare até se orgulhar.",
        "A meta não é ser perfeito, é ser constante.",
        "Se fosse fácil, todo mundo faria.",
        "Você não precisa ter pressa, precisa ter propósito.",
        "Um bom dia começa com uma boa atitude.",
        "A vitória ama o esforço.",
        "O amanhã é construído hoje.",
        "Nada é em vão, tudo é aprendizado.",
        "Acredite mais em si mesmo e menos nas circunstâncias."
]
    frase_do_dia = random.choice(frases)
    return frase_do_dia


@app.route("/")
def home():
    noticias = Noticia.query.all() #pegando todas as rows do nosso banco
    clima_guarulhos = clima_hoje()
    hoje = dia_de_hoje()
    frase_do_dia = gerador_de_frase()
    return render_template("index.html", noticias=noticias, clima=clima_guarulhos, hoje=hoje, frase_do_dia=frase_do_dia)
    

@app.route("/admin")
def admin():
    noticias = Noticia.query.all()
    clima_guarulhos = clima_hoje()
    hoje = dia_de_hoje()
    frase_do_dia = gerador_de_frase()
    return render_template("admin.html", noticias=noticias, clima=clima_guarulhos, hoje=hoje, frase_do_dia=frase_do_dia)

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

    app.run(host="0.0.0.0",debug=True)