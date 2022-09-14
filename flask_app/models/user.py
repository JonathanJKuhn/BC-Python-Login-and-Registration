from flask_app.config.mysqlconnection import connectToMySQL

class User:
    def __init__(self, db_data) -> None:
        self.id = db_data['id']
        self.fname = db_data['first_name']
        self.lname = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.dob = db_data['date_of_birth']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @staticmethod
    def add(data):
        query = "INSERT INTO users (first_name,last_name,email,password,date_of_birth) VALUES (%(fname)s,%(lname)s,%(email)s,%(password)s,%(dob)s);"
        result = connectToMySQL('login_schema').query_db(query, data)
        return result