import sqlite3
from flask import Flask, render_template
from db import db
from models import Noticia


app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)