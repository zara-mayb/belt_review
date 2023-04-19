from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under = data['under']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def create_one(cls,data):
        query = "INSERT INTO recipes (name, description, instructions, under, date_made, user_id) "
        query += "VALUES (%(name)s, %(description)s, %(instructions)s, %(under)s, %(date_made)s, %(user_id)s);"
        result = connectToMySQL(DATABASE).query_db( query,data )

    @classmethod
    def get_all_with_users(cls):
        query = "SELECT * FROM recipes r JOIN users u ON r.user_id = u.id;" 
        results = connectToMySQL(DATABASE).query_db(query)
        list_of_recipes = []
        for row in results:
            current_recipe = cls (row)
            recipe_user = {
                **row,
                "created_at": row["u.created_at"],
                "updated_at": row["u.updated_at"],
                "id": row["u.id"],
            }
            current_recipe.user = user_model.User(recipe_user)
            list_of_recipes.append(current_recipe)
        return list_of_recipes

    @classmethod
    def get_one_with_user( cls, data ):
        query = "SELECT * FROM recipes r JOIN users u ON r.user_id = u.id WHERE r.id = %(id)s; "
        results = connectToMySQL(DATABASE).query_db(query, data)
        row = results[0]
        current_recipe = cls( row )
        recipe_user = {
            "created_at": row["u.created_at"],
            "updated_at": row["u.updated_at"],
            "id": row["u.id"],
            **row
        }
        current_recipe.user = user_model.User(recipe_user)
        return current_recipe

    @classmethod
    def delete_one(cle,data):
        query = "DELETE FROM recipes WHERE id = %(id)s; "
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one( cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s; "
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])

    @classmethod
    def update_one(cls,data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under = %(under)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len( data["name"]) == 0:
            flash("You must provide a name!", "error_name")
            is_valid = False
        if len( data["description"]) == 0:
            flash("You must provide a description!", "error_description")
            is_valid = False
        if len( data["instructions"]) == 0:
            flash("You must provide a instructions!", "error_instructions")
            is_valid = False
        return is_valid