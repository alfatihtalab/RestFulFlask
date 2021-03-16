import sqlite3
from flask_restful import Resource, reqparse

class User():
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password


    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query,(username,))
        raw = result.fetchone()

        if raw:
            user = cls(*raw)
        else:
            user = None
        
        
        connection.close()
        return user
    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(query,(id,))
        raw = result.fetchone()

        if raw:
            user = cls(*raw)
        else:
            user = None
        return user
        connection.close()
        connection.commit()
    

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username', type=str, required=True, help="this can not be blank"
    )
    parser.add_argument(
        'password', type=str, required=True, help="this can not be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        
        insert_query = "INSERT INTO users VALUES(Null, ?,?)"

        if User.find_by_username(data['username']):
            return {"message": "An user with this username is already exists"}, 400


        else:
            
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute(insert_query,(data['username'], data['password']))
            connection.commit()
            connection.close()
            return {"message": "successfully added"} ,201

class AllUsers(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users"

        users = cursor.execute(query)
        list = []
        for row in users:
            list.append({'name': row[1], 'password': row[2]})
        connection.commit()
        connection.close()
            
        return list 



    