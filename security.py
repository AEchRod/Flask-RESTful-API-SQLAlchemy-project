from hmac import compare_digest #compare_digest returns a==b
from models.usermodel import UserModel

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and compare_digest(user.password, password): #here, compare_digest checks that user password is the same as the password in authenticate func.
        return user


def identity(payload):
    user_id = payload['identity'] #this contains the user's id saved into JWT
    return UserModel.find_by_id(user_id)
