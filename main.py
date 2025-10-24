import sqlite3
from flask import Flask, render_template, request, redirect
from db import db
from models import Noticia


app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/nova_noticia", methods=['GET', 'POST'])
def nova_noticia():
    if request.method == 'GET':
        return render_template("nova-noticia.html")
    else:
        titulo = request.form['tituloForm']
        capa = request.form['imgForm']
        link = request.form['urlForm']

        return redirect('admin')
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)