from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from pprint import pprint

DATABASE = 'paintings_redbelt'

class Painting:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        if 'first_name' in data:
            self.user = data['first_name']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # ! CREATE
    @classmethod
    def save(cls, data:dict) -> int:
        query = "INSERT INTO paintings (title,description,price, user_id) VALUES (%(title)s,%(description)s,%(price)s, %(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM paintings;"
        results = connectToMySQL(DATABASE).query_db(query)
        paintings = []
        for u in results:
            paintings.append( cls(u) )
        return paintings

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all_with_users(cls) -> list:
        query = "SELECT * FROM paintings JOIN users ON paintings.user_id = users.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        paintings = []
        for u in results:
            paintings.append( cls(u) )
        return paintings
    
    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data:dict) -> object:
        query  = "SELECT * FROM paintings WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return cls(result[0])

    @classmethod
    def get_one_with_user(cls,data:dict) -> object:
        query  = "SELECT * FROM paintings LEFT JOIN users ON paintings.user_id = users.id  WHERE paintings.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return cls(result[0])

    # ! UPDATE
    @classmethod
    def update(cls,data:dict) -> int:
        query = "UPDATE paintings SET title=%(title)s,description=%(description)s,price=%(price)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    # ! DELETE
    @classmethod
    def destroy(cls,data:dict):
        query  = "DELETE FROM paintings WHERE id = %(id)s;"
        connectToMySQL(DATABASE).query_db(query,data)

    @staticmethod
    def add_painting(painting:dict) -> bool:
        is_valid = True # ! we assume this is true
        if len(painting['title']) < 2:
            flash("Title must be at least 2 characters.")
            is_valid = False
        if len(painting['description']) < 10:
            flash("Description must be at least 10 characters.")
            is_valid = False
        if not len(painting['price']) > 0:
            flash("Price must be greater than 0 characters.")
            is_valid = False
        return is_valid