from db import db
from equitymodel import EquityModel

class PortfolioModel(db.Model):

    __tablename__ = "Portfolio"

#we inherit from the equity model so name/price cannot be modified.

    equity = EquityModel.name
    price = EquityModel.price

    def __init__(self, equity, price):
        self.equity = equity #self.equity for this class
        self.price = price

    def json(self):
        return {"equity": self.equity, "price": self.price}

    @classmethod
    def find_by_name(cls): #or find_by_name(cls, equity)
        name = cls.equity
        return EquityModel.find_by_name(name)

    def save_to_db(self):
        db.session.add(self) #it adds our model to database

        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)

        db.session.commit()



