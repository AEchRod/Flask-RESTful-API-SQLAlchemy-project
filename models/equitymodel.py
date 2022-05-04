from db import db #this imports SQLAlchemy

class EquityModel(db.Model): #db.Model means that we are retrieving this class from a database.

    __tablename__ = 'equities' #note __tablename__ changes from Resource

    id = db.Column(db.Integer, primary_key=True) #we define data type first and then we set this to be the primary key.
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2)) #precision equals the amount of numbers after the decimal.

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self): #this returns a json representation of model
        return {'name': self.name, 'price': self.price} #a dictionary representing our item

    @classmethod #this should still be a classmethod.
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #.query comes from db.Model, a query builder. #SELECT * FROM __tablename__ WHERE name=name LIMIT 1.
        #we use cls above instead of EquityModel since this is a classmethod.

    def save_to_db(self):  #this is no longer a class method since it calls itself.

        db.session.add(self)
        # it saves model to database, we do not need to tell SQLAlchemy which row to insert, just object (self).
        db.session.commit()

    def delete_from_db(self):

        db.session.delete(self)
        # it saves model to database, we do not need to tell SQLAlchemy which row to insert, just object (self).
        db.session.commit()
