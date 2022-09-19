from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from flask_app.controllers.paintings import Painting


DATABASE = 'paintings_redbelt'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data:dict ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.paintings = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data:dict ) -> int:
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def update(cls, data:dict ) -> int:
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE users.id = %(id)s;"
        connectToMySQL(DATABASE).query_db( query, data )


    ## ! used in user validation
    @classmethod
    def get_by_email(cls,data:dict) -> object or bool:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_one_with_painting(cls,data:dict) -> object:
        query  = "SELECT * FROM users JOIN paintings ON paintings.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        print('*'*20)
        print(results)
        print('*'*20)
        user = cls(results[0])
        
        for result in results:
            sub_data = {
                'id': result['paintings.id'],
                'title': result['title'],
                'description': result['description'],
                'price' : result['price'],
                'user_id': result['user_id'],
                'created_at': result['paintings.created_at'],
                'updated_at': result['paintings.updated_at']
            }
            user.paintings.append(Painting(sub_data))
        return user


    # ! show
    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data:dict) -> object:
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return cls(result[0])


    @staticmethod
    def validate_user(user:dict) -> bool:
        is_valid = True # ! we assume this is true
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if not len(user['password']) >= 8:
            flash("Passwords must be minimum 8 characters long")
            is_valid = False
        if user['password'] != user['confirm-password']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid
    
    @staticmethod
    def update_user(user:dict) -> bool:
        is_valid = True # ! we assume this is true
        if len(user['first_name']) < 2:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 10:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid