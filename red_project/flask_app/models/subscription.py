from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint

DATABASE = 'red_belt'

class Subscription:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        if 'first_name' in data:
            self.user = data['first_name']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # ! CREATE
    @classmethod
    def save(cls, data:dict) -> int:
        query = "INSERT INTO subscriptions (title,description, user_id) VALUES (%(title)s,%(description)s, %(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM subscriptions;"
        results = connectToMySQL(DATABASE).query_db(query)
        subscriptions = []
        for u in results:
            subscriptions.append( cls(u) )
        return subscriptions

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all_with_users(cls) -> list:
        query = "SELECT * FROM subscriptions JOIN users ON subscriptions.user_id = users.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        subscriptions = []
        for u in results:
            subscriptions.append( cls(u) )
        return subscriptions
    
    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data:dict) -> object:
        query  = "SELECT * FROM subscriptions WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return cls(result[0])

    @classmethod
    def get_one_with_user(cls,data:dict) -> object:
        query  = "SELECT * FROM subscriptions LEFT JOIN users ON subscriptions.user_id = users.id  WHERE subscriptions.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return cls(result[0])

    # ! UPDATE
    @classmethod
    def update(cls,data:dict) -> int:
        query = "UPDATE subscriptions SET title=%(title)s,description=%(description)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    # ! DELETE
    @classmethod
    def destroy(cls,data:dict):
        query  = "DELETE FROM subscriptions WHERE id = %(id)s;"
        connectToMySQL(DATABASE).query_db(query,data)