from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

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

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('login_schema').query_db(query, data)
        print(result[0])
        return cls(result[0])

    @staticmethod
    def validate_registration(user):
        is_valid = True
        if len(user['fname']) <= 0:
            flash("First Name must not be empty.")
            is_valid = False
        if len(user['lname']) <= 0:
            flash("Last Name must not be empty.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.")
            is_valid = False
        if len(user['password']) <= 0:
            flash("Password must not be empty.")
            is_valid = False
        if len(user['confirm']) <= 0:
            flash("Please confirm password.")
            is_valid = False
        if not user['password'] == user['confirm']:
            flash("Password does not match Confirm Password.")
            is_valid = False

        if is_valid:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            result = connectToMySQL('login_schema').query_db(query, user)
            if result:
                flash("Email already exists.")
                is_valid = False
        return is_valid