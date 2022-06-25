from flask_restful import Resource, reqparse
from models.usermodel import UserModel
from hmac import compare_digest
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from blacklist import BLACKLIST


#from Twilio import message

#THE CODE PREVIOUSLY HERE WASN'T A RESOURCE SO IT NEEDS TO BE MOVED TO THE MODELS PACKAGE/FOLDER.

#we bring the parser here since it was duplicated in two of our classes.
#The underscore at the beginning, tells other users they shouldn't be importing this from anywhere else.

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                    )
_user_parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                    )

class UserRegister(Resource): #modifying user register in database.

    TABLE_NAME = 'users'

    @jwt_required
    def post(self):
        # we get data from parser that was sent to us
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']): #i.e. if it finds an username by the username given in the parsed JSON.
            return {'message': 'A user with that username already exists'}

        #this saves the new user with it's given username and password.
        user = UserModel(**data)  #same as -> UserModel(data['username'], data['password']), i.e. a user variable created by the given data.
        user.save_to_db()

        return {'message': 'User saved to database'}, 201


class User(Resource):

    #Reminder: GET method requesting JSON data from server.
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id) #this takes the user_id variable and applies it to UserModel.
        if not user:
            return {"message": "User not found"}, 404
        return user.json(), 200 #this return json method from user

    @classmethod
    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        UserModel.delete_from_db()

        return {"message": "User successfully deleted."}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):

        #get data from parser
        data = _user_parser.parse_args()

        #if we find user in database based on parsed data
        user = UserModel.find_by_username(data['username'])

        # check password
        if user and compare_digest(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True) #identity stores data in JWT
            refresh_token = create_refresh_token(user.id) #user.id is our identity here
            # A refresh token is a long lived JWT that can only be used to creating new access tokens.
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200, #or alternatively, jsonify(access_token=access_token, refresh_token=refresh_token)
            #Twilio.message

        return {"message": "Invalid credentials."}, 401 #code 401 means unathorized.


class UserLogout(Resource):
    @jwt_required()
    def post(self): #we just want to blacklist user's JWT, not identity.
        jti = get_jwt()['jti'] #jti = jwt id
        BLACKLIST.add(jti) #BLACKLIST is a set, so we can .add to set.
        return {'message': 'Successfully logged out.'}, 200


class TokenRefresh(Resource): #post since it receives data in the headers in Postman.

    # We are using the `refresh=True` options in jwt_required to only allow
    # refresh tokens to access this route.

    @jwt_required(refresh=True) #A refresh token is a long lived JWT that can only be used to creating new access tokens.
    def TokenRefresher(self):
        current_user = get_jwt_identity() #variable that stores the identity of current user using refresh token.
        new_token = create_access_token(identity=current_user, fresh=False) #we create a new token with user's identity.
        #if fresh=True, the user would create fresh tokens by refreshing.
        #this means the jwt token could be from a couple of days ago.
        return {'access_token': new_token}, 200





