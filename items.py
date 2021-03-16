import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import request, jsonify


class Item(Resource):

    @classmethod
    def find_item_by_name(cls,name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        get_query = "SELECT * FROM items where name = ?"
        result = cursor.execute(get_query,(name,))
        row = result.fetchone()
        conn.close()
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @classmethod
    def insert(cls,item):
        item = {'name':item['name'], 'price':item['price']}
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        insert_query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(insert_query,(item['name'],item['price']))
        conn.commit()
        conn.close()
    @classmethod
    def update(cls,item):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        update_query = "UPDATE items SET price=? where name=?"
        cursor.execute(update_query,(item['price'],item['name']))
        conn.commit()
        conn.close()
       

    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        # return {'message': 'item not found'}, 404
        item = self.find_item_by_name(name)
        if item:
            return item
        else:
            return {'message': 'item not found'}
        

    def post(self,name):
        # if next(filter(lambda x: x['name'] == name, items), None):
        #     return {'message': 'an item with name {} already exists !'.format(name)}, 400
        # data = request.get_json()
        # new_item = {'name': name, 'price': data['price']}
        # items.append(new_item)
        # return new_item, 201
        item = self.find_item_by_name(name)
        if item:
            return {'message': 'item with name {} an exists item try another!'.format(name)}
        else:
            try:
                data = request.get_json()
                new_item = {'name': name, 'price': data['price']}
                self.insert(new_item)
                return {'message': 'good it has been add to the database'}, 200
            except:
                return {'message': 'error not inserted'} , 500
        



    def delete(self, name):
        item = self.find_item_by_name(name)
        if item:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items where name = ?",(name,))
            conn.commit()
            conn.close()
            return {"message ": "item with name {} deleted ".format(name)}
        return {'message': 'item with name {} not found'.format(name)}

    def put(self, name):
        # parser = reqparse.RequestParser()
        # parser.add_argument(
        #     'price',
        #     type=float,
        #     required=True,
        #     help='this is rquired '
        # )
        # data = parser.parse_args()

        # item = next(filter(lambda x: x['name'] == name, items), None)
        # if item is None:
        #     item = {'name': name, 'price': data['price']}
        #     items.append(item)
        # else:
        #     item.update(data)
        # return item
        data = request.get_json()
        item = self.find_item_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item:
            try:
                self.update(updated_item)
                return {'message': 'item with name {} has been updated'.format(name)}
            except:
                return {'message': 'not updated try again'}, 500
        else:
            try:
                self.insert(updated_item)
            except:
                return {'message': 'not inserted try again'}, 500

            


class ItemList(Resource):
    def get(self):
        items = []
        
        try:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            itemList = cursor.execute("SELECT * FROM items")

            if itemList:
                for row in itemList:
                    items.append({'name':row[0], 'price': row[1]})
                return {'items': items}
            else:
                return {'items': 'no items found'}
        except:
            return {'message': "error"}

