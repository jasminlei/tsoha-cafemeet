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


def update_profile():
    username = session.get("username")
    favourite_food = request.form.get("favorite_food")
    bio = request.form.get("bio")
    fav_food_error = False
    bio_error = False
    if len(favourite_food) > 100:
        fav_food_error = True
    if len(bio) > 1000:
        bio_error = True
    if not fav_food_error and not bio_error:
        sql = text("""
                UPDATE user_profiles
                SET favorite_food = :favorite_food, bio = :bio
                FROM users
                WHERE user_profiles.user_id = users.id
                AND users.username = :username
            """)
        db.session.execute(
            sql, {"favorite_food": favourite_food, "bio": bio, "username": username}
        )
        db.session.commit()
        return True, fav_food_error, bio_error
    return False, fav_food_error, bio_error
