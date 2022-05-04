from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.usermodel import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )

    @jwt_required
    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']): #i.e. if it finds an username by the username given in the parsed JSON.
            return {'message': 'A user with that username already exists'}

        #this saves the new user with it's given username and password.
        user = UserModel(**data)  #same as -> UserModel(data['username'], data['password']), i.e. a user variable created by the given data.
        user.save_to_db()

        return {'message': 'User saved to database'}, 201

