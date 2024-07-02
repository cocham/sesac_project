from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    birthday = db.Column(db.Date)
    address = db.Column(db.Text)

class Store(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(40))
    type = db.Column(db.String(20))
    address = db.Column(db.Text)

class Order(db.Model):
    id = db.Column(db.String, primary_key=True)
    orderat = db.Column(db.DateTime)
    storeid = db.Column(db.String,db.ForeignKey('store.id'))
    userid = db.Column(db.String,db.ForeignKey('user.id'))

class Item(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(40))
    type = db.Column(db.String(20))
    unitprice = db.Column(db.Integer)

class Orderitem(db.Model):
    id = db.Column(db.String, primary_key=True)
    orderid = db.Column(db.String,db.ForeignKey('order.id'))
    itemid = db.Column(db.String,db.ForeignKey('item.id'))