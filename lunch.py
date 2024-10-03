import users
from flask import session, request
from sqlalchemy import text
from db import db
from datetime import datetime, timedelta


def create_lunch_post(username):
    user_id = users.get_user_id(username)
    campus = request.form.get("campus")
    restaurant = request.form.get("restaurant")
    lunch_time = request.form.get("lunch_time")
    message = request.form.get("message")
    visibility = request.form.get("visibility")

    lunch_time = datetime.strptime(lunch_time, "%Y-%m-%dT%H:%M")

    sql = text("""
        INSERT INTO lunch_posts (user_id, campus, restaurant, lunch_time, lunch_message, visibility)
        VALUES (:user_id, :campus, :restaurant, :lunch_time, :message, :visibility)
        """)

    db.session.execute(
        sql,
        {
            "user_id": user_id,
            "campus": campus,
            "restaurant": restaurant,
            "lunch_time": lunch_time,
            "message": message,
            "visibility": visibility,
        },
    )

    db.session.commit()

    return None


def latest_lunch_posts():
    current_user = session.get("username")
    current_user_id = users.get_user_id(current_user)
    if current_user:
        sql = text("""
                SELECT u.username, lp.user_id, to_char(lp.lunch_time, 'DD.MM.YYYY, HH24:MI') AS lunch_time, lp.restaurant, lp.campus, lp.lunch_message, lp.visibility, to_char(lp.created_at, 'DD.MM.YYYY, HH24:MI') AS created_at, lp.id, COUNT(lr.id) AS comment_count
                FROM lunch_posts lp
                JOIN  users u ON lp.user_id = u.id 
                LEFT JOIN lunch_responses lr ON lp.id = lr.post_id
                WHERE lp.visibility = 'public' OR lp.user_id = :current_user_id 
                   OR (lp.visibility = 'friends' AND EXISTS (
                        SELECT 1 
                        FROM friends 
                        WHERE (user1 = :current_user_id AND user2 = lp.user_id AND status = 'accepted') 
                        OR (user1 = lp.user_id AND user2 = :current_user_id AND status = 'accepted')))
                GROUP BY 
                lp.id, u.username, lp.user_id, lp.lunch_time, lp.restaurant, lp.campus, lp.lunch_message, lp.visibility, lp.created_at
                ORDER BY 
                lp.created_at DESC 
                LIMIT 5;
            """)
        result = db.session.execute(
            sql, {"current_user_id": current_user_id} if current_user_id else {}
        )
        latest_posts = result.fetchall()

        return latest_posts

    else:
        sql = text("""
            SELECT u.username, lp.user_id, to_char(lp.lunch_time, 'DD.MM.YYYY, HH24:MI') AS lunch_time, lp.restaurant, lp.campus, lp.lunch_message, lp.visibility, to_char(lp.created_at, 'DD.MM.YYYY, HH24:MI') AS created_at
            FROM lunch_posts lp
            JOIN users u ON lp.user_id = u.id 
            WHERE lp.visibility = 'public'
            ORDER BY lp.lunch_time DESC 
            LIMIT 5
        """)

    result = db.session.execute(sql)
    latest_posts = result.fetchall()
    return latest_posts


def all_lunch_posts():
    current_user = session.get("username")
    current_user_id = users.get_user_id(current_user)
    sql = text("""
                SELECT u.username, lp.user_id, to_char(lp.lunch_time, 'DD.MM.YYYY, HH24:MI') AS lunch_time, lp.restaurant, lp.campus, lp.lunch_message, lp.visibility, to_char(lp.created_at, 'DD.MM.YYYY, HH24:MI') AS created_at, lp.id, COUNT(lr.id) AS comment_count
                FROM lunch_posts lp
                JOIN  users u ON lp.user_id = u.id 
                LEFT JOIN lunch_responses lr ON lp.id = lr.post_id
                WHERE lp.visibility = 'public' OR lp.user_id = :current_user_id 
                   OR (lp.visibility = 'friends' AND EXISTS (
                        SELECT 1 
                        FROM friends 
                        WHERE (user1 = :current_user_id AND user2 = lp.user_id AND status = 'accepted') 
                        OR (user1 = lp.user_id AND user2 = :current_user_id AND status = 'accepted')))
                GROUP BY 
                lp.id, u.username, lp.user_id, lp.lunch_time, lp.restaurant, lp.campus, lp.lunch_message, lp.visibility, lp.created_at
                ORDER BY 
                lp.created_at DESC 
                """)
    result = db.session.execute(sql, {"current_user_id": current_user_id})
    all_posts = result.fetchall()

    return all_posts


def one_post(id):
    sql = text("""
            SELECT u.username, lp.user_id, to_char(lp.lunch_time, 'DD.MM.YYYY, HH24:MI') AS lunch_time, lp.restaurant, lp.campus, lp.lunch_message, lp.visibility, to_char(lp.created_at, 'DD.MM.YYYY, HH24:MI') AS created_at, lp.id
            FROM lunch_posts lp
            JOIN users u ON lp.user_id = u.id 
            WHERE lp.id = :id
            """)

    result = db.session.execute(sql, {"id": id})
    post_data = result.fetchone()

    return post_data


def comment_post(post_id):
    comment = request.form.get("comment")
    user_id = users.get_user_id(session["username"])
    sql = text("""
            INSERT INTO lunch_responses (post_id, user_id, message)
            VALUES (:post_id, :user_id, :message)
        """)
    db.session.execute(
        sql, {"post_id": post_id, "user_id": user_id, "message": comment}
    )
    db.session.commit()
    return None


def show_comments(id):
    sql = text("""
    SELECT u.username, lr.message, to_char(lr.created_at, 'DD.MM.YYYY, HH24:MI') AS created_at
    FROM lunch_responses lr
    JOIN users u ON lr.user_id = u.id
    WHERE lr.post_id = :post_id
    ORDER BY lr.created_at ASC
    """)

    result = db.session.execute(sql, {"post_id": id})
    comments = result.fetchall()

    return comments


def number_of_comments(id):
    sql = text("""
            SELECT COUNT (*)
            FROM lunch_responses
            WHERE lr.post_id = :post_id
            """)

    result = db.session.execute(sql, {"post_id": id})
    count = result.scalar()

    return count


def edit_post():
    return None


def max_week():
    now = datetime.now()
    one_week_from_now = now + timedelta(weeks=1)
    min_date = now.strftime("%Y-%m-%dT%H:%M")
    max_date = one_week_from_now.strftime("%Y-%m-%dT%H:%M")

    return min_date, max_date
