from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models.user import User
import re 
from flask import flash


db = 'sasquatch'

class Sighting:
    db = 'sasquatch'
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.date = data['date']
        self.what_happened = data['what_happened']
        self.amount = data['amount']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.reporter_first_name = User.get_one({'id':data['user_id']}).first_name
        self.reporter_last_name = User.get_one({'id':data['user_id']}).last_name
        self.number_of_skeptics = Sighting.get_number_of_skeptics({'id':data['user_id']})


    @classmethod
    def save(cls, data):
        query = "INSERT INTO sightings(location, date, what_happened, amount, user_id) VALUES (%(location)s, %(date)s, %(what_happened)s, %(amount)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM sightings WHERE id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
    
        return cls(result[0])
    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        results = connectToMySQL('sasquatch').query_db(query)
        sasquatchs= []
        for sasquatch in results:
            sasquatchs.append(cls(sasquatch))

        return sasquatchs
    
    @classmethod
    def update(cls, data):
        query = "UPDATE sightings SET location = %(location)s, date = %(date)s, what_happened = %(what_happened)s, amount = %(amount)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    

    @staticmethod
    def validate_sighting(data):
        is_valid = True
        for key, value in data.items():
            if len(value) < 1:
                flash("All fields are required.")
                is_valid = False
                return is_valid
        if int(data['amount']) < 1:
            flash('Amount cannot be less than 1')
            is_valid = False
            
        return is_valid
    

    @classmethod
    def create_skeptic(cls, data):
        query = "INSERT INTO skeptics(sighting_id, user_id) VALUES (%(sighting_id)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    

    @classmethod
    def delete_skeptic(cls, data):
        query = "DELETE FROM skeptics WHERE sighting_id = %(sighting_id)s AND user_id = %(user_id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    

    @classmethod
    def get_number_of_skeptics(cls, data):
        query = "SELECT COUNT(*) FROM skeptics WHERE sighting_id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            return 0
        return result[0]['COUNT(*)']


    @classmethod
    def get_users_that_are_skeptic(cls, data):
        query = "SELECT skeptics.user_id, users.first_name, users.last_name FROM skeptics LEFT JOIN users ON skeptics.user_id = users.id WHERE sighting_id = %(id)s;"
        results = connectToMySQL('sasquatch').query_db(query, data)
        if not results:
            return []
        return results
    

    @classmethod
    def is_user_skeptic(cls, data):
        query = "SELECT * FROM skeptics WHERE sighting_id = %(sighting_id)s AND user_id = %(user_id)s;"
        results = connectToMySQL('sasquatch').query_db(query, data)
        if not results:
            return False
        return True
        

