from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.equity import Equity, Portfolio
from resources.user import UserRegister
from security import identity, authenticate



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #this indicates where the database is located.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #we turn this off to save resources (Flask SQLAlchemy tracker) and SQLAlchemy has own modification tracker.
app.config['PROPAGATE_EXCEPTIONS'] = True #this returns specific errors.
app.secret_key = 'asdf'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth (endpoint)


api.add_resource(Equity, '/equities/<string:name>')
api.add_resource(Portfolio, '/portfolio')
api.add_resource(UserRegister, '/register')


if __name__ == "main":
    from db import db
    db.init_app(db) #we pass our Flask app here to avoid circular imports.
    app.run(port=5000, debug= True) #debug= True means that we won't have to restart our app every time we make a change.







