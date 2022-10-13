import sys

sys.path.insert(1, r'/Users/andresecheverry/Documents/Coding/Flask/ChafAPIRESTfulSQL/resources')

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import User, UserLogin, UserLogout, UserRegister, TokenRefresh
from resources.equity import Equity, Portfolio
from blacklist import BLACKLIST


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #this indicates where the database is located.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #we turn this off to save resources (Flask SQLAlchemy tracker) and SQLAlchemy has own modification tracker.
app.config['PROPAGATE_EXCEPTIONS'] = True #this returns specific errors.
api = Api(app)

#jwt = JWT(app, authenticate, identity) # /auth (endpoint)
app.config['JWT_BLACKLIST_ENABLED'] = True #this enables the blacklisting process
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh'] #we enable blacklist for both access and refresh token
app.secret_key = 'asdf'
jwt = JWTManager(app)
#WE NOW CREATE /AUTH IN USER RESOURCE

@jwt.additional_claims_loader #this decorator links function below to JWTManager
def add_claims_to_jwt(identity): #remember identity is user.id
    if identity == 1: #i.e. if user is first one to be created in db = admin. SHOULD READ FROM CONFIG FILE OR DATABASE.
        return {'is_admin': True}
    return {"is_admin": False} #otherwise

@jwt.token_in_blocklist_loader
def check_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST #if True, revoked token callback.

@jwt.expired_token_loader #jwt here is the variable we created above
#this applies when JWT token has expired
def expired_token_callback():
    return jsonify({'description': 'The token has expired',
                    'error': 'token_expired' #this shows instead of the usual Flask message
                    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return ({
        'description': 'Signature verification received.',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return ({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401

@app.before_first_request #this decorator affects the method below it.
def create_tables():
    db.create_all() #this functions will run before the first request and will create the data.db file.


api.add_resource(Equity, '/equities/<string:name>')
api.add_resource(Portfolio, '/portfolio')
api.add_resource(User, '/user/<int:user_id>') #since user id is an integer, this is what we pass to endpoint.
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == "main":
    from db import db
    db.init_app(db) #we pass our Flask app here to avoid circular imports.
    app.run(port=5000, debug= True) #debug= True means that we won't have to restart our app every time we make a change.







