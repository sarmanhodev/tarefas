from main import db, app
from flask_login import UserMixin
from sqlalchemy import Text


class Alunos (db.Model, UserMixin):
    __tablename__ = "alunos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(256), unique = True, nullable= False)
    email = db.Column(db.String(50), unique = True, nullable=False)
    telefone = db.Column(db.String(256), unique = True, nullable= True)
    idade = db.Column(db.Integer, unique=False, nullable = False)
    data_nascimento = db.Column(db.String(256), unique=False, nullable = False)


class Post(db.Model,UserMixin):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    data_post = db.Column(db.String(50), unique = False, nullable=False)
    data_limite = db.Column(db.String(50), unique = False, nullable=False)
    data_conclusao = db.Column(db.String(50), unique = False, nullable=True)
    observacoes = db.Column(db.Text, unique = False, nullable = False)
    assunto = db.Column(db.String(256), unique = True, nullable= True)
    post_status_id = db.Column(db.Integer,db.ForeignKey("post_status.id"), unique=False)

    post_post_status = db.relationship('Post_Status', back_populates = 'post_status_post', lazy = True)


class Post_Status(db.Model,UserMixin):
    __tablename__ = 'post_status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), unique = False, nullable=False)

    post_status_post = db.relationship('Post', back_populates= 'post_post_status', lazy = True)

