from sqlalchemy import text
from db import db


def is_friend(current_user, profile_username):
    sql = text("""
        SELECT COUNT(*)
        FROM friends f
        JOIN users u1 ON f.user1 = u1.id
        JOIN users u2 ON f.user2 = u2.id
        WHERE ((u1.username = :current_user AND u2.username = :profile_username)
        OR (u1.username = :profile_username AND u2.username = :current_user))
        AND f.status = 'accepted'
    """)
    result = db.session.execute(
        sql, {"current_user": current_user, "profile_username": profile_username}
    )
    count = result.scalar()
    return count > 0


def is_pending(current_user, profile_username):
    sql1 = text("""
        SELECT COUNT(*)
        FROM friends f
        JOIN users u1 ON f.user1 = u1.id
        JOIN users u2 ON f.user2 = u2.id
        WHERE (u1.username = :current_user AND u2.username = :profile_username
        AND f.status = 'pending')
    """)
    result = db.session.execute(
        sql1, {"current_user": current_user, "profile_username": profile_username}
    )
    count = result.scalar()
    if count > 0:
        return True, "you_have_already_requested"

    sql2 = text("""
        SELECT COUNT(*)
        FROM friends f
        JOIN users u1 ON f.user1 = u1.id
        JOIN users u2 ON f.user2 = u2.id
        WHERE (u2.username = :current_user AND u1.username = :profile_username
        AND f.status = 'pending')
    """)
    result = db.session.execute(
        sql2, {"current_user": current_user, "profile_username": profile_username}
    )
    count = result.scalar()
    if count > 0:
        return True, "this_user_wants_to_be_friend"
    return False, ""


def add_friend(current_user, other_user):
    sql = text("""
        INSERT INTO friends (user1, user2, status)
        SELECT u1.id, u2.id, 'pending'
        FROM users u1, users u2
        WHERE u1.username = :current_user
          AND u2.username = :other_user
    """)

    db.session.execute(sql, {"current_user": current_user, "other_user": other_user})
    db.session.commit()

    return None


def accept_friend_request(current_username, friend_username):
    sql = text("""
        UPDATE friends
        SET status = 'accepted'
        FROM users u1, users u2
        WHERE friends.user1 = u1.id
          AND friends.user2 = u2.id
          AND u1.id = :friend_user_id
          AND u2.username = :current_username
          AND friends.status = 'pending'
    """)

    db.session.execute(
        sql, {"current_username": current_username, "friend_user_id": friend_username}
    )
    db.session.commit()

    return None


def show_friend_requests(user):
    sql = text("""
        SELECT f.user1, u.username
        FROM friends f
        JOIN users u ON u.id = f.user1
        JOIN users u2 ON u2.id = f.user2
        WHERE f.status = 'pending' AND u2.username = :user
    """)

    result = db.session.execute(sql, {"user": user})
    return result.fetchall()


def show_friends(user):
    sql = text("""
        SELECT u.username, u2.username
        FROM friends f
        JOIN users u ON u.id = f.user1
        JOIN users u2 ON u2.id = f.user2
        WHERE f.status = 'accepted' AND (u2.username = :user OR u.username =:user)
    """)

    result = db.session.execute(sql, {"user": user})
    friends = result.fetchall()

    filtered_friends = set()
    for friend1, friend2 in friends:
        if friend1 != user:
            filtered_friends.add(friend1)
        if friend2 != user:
            filtered_friends.add(friend2)

    return list(filtered_friends)


def remove_friend():
    return None
