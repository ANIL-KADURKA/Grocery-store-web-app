from database import db
from sqlalchemy import DateTime
from sqlalchemy import Column,Integer,String,JSON,ForeignKey
from datetime import datetime
# from flask_login import UserMixin

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))
    status=db.Column(db.String(20))
    cart = db.Column(db.JSON())               

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer)
    rate = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"))
    store_manager_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))
    units = db.Column(db.String(20))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    quantity = db.Column(db.Float)
    amount= db.Column(db.Float)
    status = db.Column(db.String)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    ordered_at = db.Column(db.DateTime, default=datetime.utcnow)
