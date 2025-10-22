from db import db

class Noticia(db.Model):
    __tablename__: 'noticias'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    capa = db.Column(db.LargeBinary, nullable=False)
    link = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<{self.titulo}>"