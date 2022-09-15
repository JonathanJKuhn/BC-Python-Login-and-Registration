from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')
PW_REGEX = re.compile(r'(?=.*\d)(?=.*[A-Z])')

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
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('login_schema').query_db(query, data)
        return cls(result[0])
        
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('login_schema').query_db(query, data)
        return cls(result[0])

    @staticmethod
    def validate_registration(user):
        is_valid = True
        if len(user['fname']) < 2:
            flash("First Name isn't long enough")
            is_valid = False
        if len(user['lname']) < 2:
            flash("Last Name isn't long enough")
            is_valid = False
        elif not NAME_REGEX.match(user['fname']) or not NAME_REGEX.match(user['lname']):
            flash("Name must only contain letters")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password isn't long enough")
            is_valid = False
        elif not PW_REGEX.match(user['password']):
            flash("Please inlcude at least 1 number and 1 uppercase letter")
            is_valid = False
        if len(user['confirm']) <= 0:
            flash("Please confirm password")
            is_valid = False
        if not user['password'] == user['confirm']:
            flash("Password does not match Confirm Password")
            is_valid = False

        if is_valid:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            result = connectToMySQL('login_schema').query_db(query, user)
            if result:
                flash("Email already exists.")
                is_valid = False
        return is_valid