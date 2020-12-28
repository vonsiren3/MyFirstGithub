# coding:utf-8

from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用户编号
    telephone = db.Column(db.String(11), nullable=False)  # 手机号
    username = db.Column(db.String(50), nullable=False)  # 用户名
    password = db.Column(db.String(100), nullable=False)  # 密码

class Good(db.Model):
    __tablename__ = "good"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 商品编号
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('goods'))

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    good = db.relationship('Good', backref=db.backref('comments', order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('comments'))

class Buycar(db.Model):
    __tablename__ = 'buycar'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('buycars'))
    good = db.relationship('Good', backref=db.backref('buycars'))

class Record(db.Model):
    __tablename__ = 'record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('records'))
    good = db.relationship('Good', backref=db.backref('records'))
