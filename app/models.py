from datetime import datetime
from . import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category {}>'.format(self.name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
                               backref=db.backref('items', lazy='dynamic'))

    def __init__(self, name, category):
        self.name = name
        self.category = category

    def __repr__(self):
        return '<Item {}({})>'.format(self.name,
                                      self.category.name)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    description = db.Column(db.String(256))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    item = db.relationship('Item',
                           backref=db.backref('records', lazy='dynamic'))

    def __init__(self, item, description, start_date=None, end_date=None):
        self.item = item
        self.description = description
        if start_date is None:
            start_date = datetime.utcnow()
        self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date

    def __repr__(self):
        return '<Record {} ({}-{})>'.format(self.item.name,
                                            self.start_date, self.end_date)
