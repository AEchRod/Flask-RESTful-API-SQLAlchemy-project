from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        #we don't need self.id since it is auto-incrementing
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first() #first username is table name by which we filter and second is argument.
        #.first() since there are no two users with the same username

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()





