from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.recipe_model import Recipe

@app.route("/recipes", methods = ["GET"])
def get_books():
    all_recipes = Recipe.get_all_with_users()
    return render_template("recipes.html", all_recipes = all_recipes)

@app.route("/recipe/form", methods = ["GET"])
def display_recipe_form():
    return render_template("recipe_form.html")

@app.route("/recipe/new", methods = ["POST"])
def add_recipe():
    data = {
        **request.form,
        "user_id": session["user_id"]
    }
    if Recipe.validate_recipe(data) == False:
        return redirect("/recipe/form")
    Recipe.create_one(data)
    return redirect("/recipes")

@app.route("/recipe/<int:id>", methods = ["GET"])
def get_recipe(id):
    data = {
        "id": id
    }
    current_recipe = Recipe.get_one_with_user(data)
    return render_template("recipe_show.html", current_recipe = current_recipe)

@app.route("/recipe/delete/<int:id>", methods = ["POST"])
def delete_recipe(id):
    data = {
        "id": id
    }
    Recipe.delete_one(data)
    return redirect("/recipes")

@app.route("/recipe/edit/<int:id>", methods = ["GET"])
def display_update_book(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id
    }
    current_recipe = Recipe.get_one(data)
    return render_template("recipe_edit.html", current_recipe = current_recipe)

@app.route("/recipe/update/<int:id>", methods = ["POST"])
def update_book(id):
    if Recipe.validate_recipe( request.form ) == False:
        return redirect( f"/recipe/edit/{id}")
    data = {
        "id": id,
        **request.form,
        "user_id": session["user_id"]
    }
    Recipe.update_one(data)
    return redirect("/recipes")

@app.route ("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")