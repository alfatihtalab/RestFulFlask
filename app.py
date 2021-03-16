from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identety
from user import User, UserRegister, AllUsers
from items import * 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
api = Api(app)

jwt = JWT(app, authenticate, identety)  # /auth



api.add_resource(Item, '/item/<string:name>')
# api.add_resource(Item, '/item/add')  #to add new item using post method 
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(AllUsers, '/users')


app.run()
