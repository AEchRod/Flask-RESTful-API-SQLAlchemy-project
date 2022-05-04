from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.equitymodel import EquityModel

#this is a resource as flask_restful works with resources.
class Equity(Resource):
    TABLE_NAME = 'equities'

    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True, #this requires a value to be passed for the argument
        help="This field cannot be left blank!"
    )

    @jwt_required
    def get(self, name):
        equity = EquityModel.find_by_name(name)
        if equity:
            return equity.json()  # this is needed since we return an object, not a dictionary.
        return {'message': 'Equity not found'}, 404

    def post(self, name):
        #note that in this function the parsed data comes searching for an equity by its name.
        if EquityModel.find_by_name(name):
            return {'message': "An equity with name '{}' already exists.".format(name)}, 400

        data = Equity.parser.parse_args() #we save the parser request into an object.

        equity = EquityModel(name, data['price']) #this retrieves the parsed data and new price for equity.

        try:
            equity.save_to_db()
        except:
            return {"message": "An error occurred inserting the equity."}

        return equity

    def delete(self, name):
        equity = EquityModel.find_by_name(name)

        if equity: #i.e. if it finds an equity, then delete from db using method from Equity model.
            EquityModel.delete_from_db()
        return {"message": "Item {} has been deleted".format(name)}


    def put(self, name):

        data = Equity.parser.parse_args() #we parse the arguments given by the request parser, i.e. updated name.

        equity = EquityModel.find_by_name(name) #we define the equity is the equity that was found by tha name

        if equity is None: #if there isn't an equity with that name, we create it and give the updated price.
            equity = EquityModel(name, data['price']) #this takes the price variable from the parsed data.
        else:
            equity.price = data['price']

        equity.save_to_db()

        return equity.json() #return json to make sure it is saved in db.

class Portfolio(Resource):
    TABLE_NAME = 'equities'

    @jwt_required
    def get(self):
        return {'equities': [equity.json() for equity in EquityModel.query.all()]}  # this retrieves JSON for all objects in database
        # this is a list comprehension for all items in the database.