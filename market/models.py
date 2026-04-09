from market import db
from sqlalchemy.orm import backref

# table 구조
class User(db.Model):
    id = db.Column(db.String(20), primary_key=True)      # user id (PK) - db 내부 구분용
    username = db.Column(db.String(50), unique=True)     # username id
    password = db.Column(db.String(20), unique=True)     # pw
    phone = db.Column(db.String(15), unique=True)        # phone number
    email = db.Column(db.String(50), unique=True)        # email

class Admin(db.Model):
    id = db.Column(db.String(20), primary_key=True)      # admin id (PK)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE', onupdate = 'CASCADE'))
    user = db.relationship('User')

class Item(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    item_name = db.Column(db.String(50), unique=True)
    item_description = db.Column(db.String(500), unique=True)
    item_price = db.Column(db.String(50), unique=True)
    status_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete = 'CASCADE', onupdate = 'CASCADE'))
    status = db.relationship('Item_status')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete = 'CASCADE', onupdate = 'CASCADE'))
    
    datetime = db.Column(db.DateTime)

class Item_status(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    status = db.Column(db.String(20), unique=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete = 'CASCADE', onupdate = 'CASCADE'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete = 'CASCADE', onupdate = 'CASCADE'))

class Category(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    category_name = db.Column(db.String(50), unique=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete = 'CASCADE', onupdate = 'CASCADE'))

class Review(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE', onupdate = 'CASCADE'))
    review_content = db.Column(db.String(500), unique=True)
    datetime = db.Column(db.DateTime)

class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete = 'CASCADE', onupdate = 'CASCADE'))
    datetime = db.Column(db.DateTime)
