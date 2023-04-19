from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user_model import User

@app.route("/")
def login_register():
    return render_template("index.html")

@app.route("/user/new", methods = ["POST"])
def create_user():
    if User.validate_registration(request.form) == False:
        return redirect("/")
    encrypted_password = User.encrypt_string(request.form["password"])
    data = {
        **request.form,
        "password": encrypted_password
    }
    user_id = User.create_one(data)
    session["user_id"] = user_id
    session["first_name"] = request.form["first_name"]
    return redirect("/recipes")

@app.route("/login", methods = ["POST"])
def process_login():
    current_user = User.get_one( request.form )
    if current_user == None:
        flash("this email does not exist in our DB", "error_login_email" )
        return redirect("/")
    if User.validate_password(request.form["password"], current_user.password) == False:
        return redirect("/")
    session["user_id"] = current_user.id
    session["first_name"] = current_user.first_name
    print("User login success" + current_user.last_name )
    return redirect ("/recipes")