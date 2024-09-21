from flask import request, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from db import db
from app import app
from os import getenv
from sqlalchemy.exc import IntegrityError


app.secret_key = getenv("SECRET_KEY")


def new_user():
    username = request.form["username"]
    password = request.form["password"]
    try:
        if len(username) > 20:
            return False, "username_too_long"
        else:
            hash_value = generate_password_hash(password)
            sql = text(
                "INSERT INTO users (username, password) VALUES (:username, :password)"
            )
            db.session.execute(sql, {"username": username, "password": hash_value})
            db.session.commit()
            sql_select = text("SELECT id FROM users WHERE username = :username")
            result = db.session.execute(sql_select, {"username": username})
            user_id = result.fetchone()[0]
            create_profile(user_id)
            return True, None
    except IntegrityError:
        return False, "username_in_use"


def create_profile(user_id):
    sql_profile = text(
        "INSERT INTO user_profiles (user_id, favorite_food, bio) VALUES (:user_id, '', '')"
    )
    db.session.execute(sql_profile, {"user_id": user_id})
    db.session.commit()


def authenticate_user():
    username = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False, "wrong_username"
    hash_value = user.password
    if check_password_hash(hash_value, password):
        session["username"] = username
        return True, None
    return False, "wrong_password"


def get_user_id(username):
    sql = text("SELECT id FROM users WHERE username = :username")
    result = db.session.execute(sql, {"username": username})
    user_id = result.scalar()
    return user_id


def user_exists(username):
    sql = text("SELECT COUNT(*) FROM users WHERE username = :username")
    result = db.session.execute(sql, {"username": username})
    return result.scalar() > 0
