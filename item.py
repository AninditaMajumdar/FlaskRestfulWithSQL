import sqlite3
from flask import Flask,request
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="this field cant be blank")

    @jwt_required()
    def get(self, name):
       item=self.find_by_name(name)
       if item:
           return item
       return {"msg": "item not found"}

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items where name =?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.commit()
        connection.close()
        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    def post(self, name):
     item = self.find_by_name(name)
     if item:
         return {"msg": "item already present"}
     else:
         data = Item.parser.parse_args() #??
         item = {"name": name,"price":data['price']}
         try:
            self.insert(item)
         except:
              return {"msg":"an error occured"},500

         return {"msg": "Added"}


    def delete(self,name):
        item = self.find_by_name(name)
        if item:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("Delete from items where name=?",(name,))
            connection.commit()
            connection.close()
            return {"msg":"deleted"}
        else:
            return {"msg" : "item not found"}


    def put(self,name): #idempotent
        item = self.find_by_name(name)
        data = Item.parser.parse_args()
        new_item = {"name": name, "price": data["price"]}
        if item:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("update items set price=? where name=?",(new_item["price"],new_item["name"]))
            connection.commit()
            connection.close()
            return {"msg": "updated"}
        else:
            self.insert(new_item)
            return {"msg": "added"}


    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO items VALUES(?,?)", (item['name'], item['price']))
        connection.commit()
        connection.close()



class ItemList(Resource):
    def get(self):
            return {'items': items}, 201
