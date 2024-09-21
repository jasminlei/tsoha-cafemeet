from flask import session, request
from sqlalchemy import text
from db import db


def profile_content(username):
    sql = text("""
        SELECT u.username, p.favorite_food, p.bio
        FROM users u
        JOIN user_profiles p ON u.id = p.user_id
        WHERE u.username = :username
    """)
    result = db.session.execute(sql, {"username": username})
    profile_data = result.fetchone()

    if profile_data:
        return profile_data
    else:
        return "", "", ""


def update_favorite_food():
    favorite_food = request.form.get("favorite_food")
    username = session.get("username")
    sql = text("""
            UPDATE user_profiles
            SET favorite_food = :favorite_food
            FROM users
            WHERE user_profiles.user_id = users.id
            AND users.username = :username
        """)
    db.session.execute(sql, {"favorite_food": favorite_food, "username": username})
    db.session.commit()
    return True


def update_bio():
    bio = request.form.get("bio")
    username = session.get("username")
    sql = text("""
            UPDATE user_profiles
            SET bio = :bio
            FROM users
            WHERE user_profiles.user_id = users.id
            AND users.username = :username
        """)
    db.session.execute(sql, {"bio": bio, "username": username})
    db.session.commit()
    return True
