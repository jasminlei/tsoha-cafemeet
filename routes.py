from app import app
import users
import profiles
import friends
import lunch
from flask import render_template, request, redirect, session, url_for


@app.route("/")
def index():
    comments_visible = False
    latest_posts = lunch.latest_lunch_posts()
    if "username" in session:
        comments_visible = True
    all_users = users.all_users()
    user_count = users.count_users()
    return render_template(
        "index.html",
        latest_posts=latest_posts,
        comments_visible=comments_visible,
        users=all_users,
        user_count=user_count,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user_created, error_message = users.new_user()
        if new_user_created:
            return redirect("/")
        return render_template("register.html", error=error_message)
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        is_authenticated, error_message = users.authenticate_user()
        if is_authenticated:
            return redirect("/")
        return render_template("login.html", error=error_message)

    if request.method == "GET":
        return render_template("login.html")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    profile_exists = users.user_exists(username)
    if request.method == "GET":
        if "username" in session:
            profile_data = profiles.profile_content(username)
            current_user = session["username"]
            if current_user == username:
                return render_template(
                    "profile.html",
                    profile_data=profile_data,
                    profile_exists=profile_exists,
                )
            is_friend = friends.is_friend(current_user, username)
            is_pending, status = friends.is_pending(current_user, username)
            friend_request = (status == "this_user_wants_to_be_friend",)

            return render_template(
                "profile.html",
                profile_data=profile_data,
                friend=is_friend,
                pending=is_pending,
                pending_status=status,
                friend_request=friend_request,
                profile_exists=profile_exists,
            )
        return render_template("profile.html", profile_exists=profile_exists)

    if request.method == "POST":
        if "add_friend" in request.form:
            current_user = session["username"]
            friends.add_friend(current_user, username)
            return redirect(f"/profile/{username}")
        return render_template("profile.html", profile_data=profile_data)


@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    username = session["username"]
    if request.method == "GET":
        profile_data = profiles.profile_content(username)
        print(profile_data)
        return render_template("edit_profile.html", content=profile_data)

    if request.method == "POST":
        if request.form.get("favorite_food"):
            favourite_food_updated = profiles.update_favorite_food()
            if favourite_food_updated:
                profile_data = profiles.profile_content(username)
                return render_template("edit_profile.html", content=profile_data)
        if request.form.get("bio"):
            bio_updated = profiles.update_bio()
            if bio_updated:
                profile_data = profiles.profile_content(username)
                return render_template("edit_profile.html", content=profile_data)


@app.route("/profile/friends", methods=["GET", "POST"])
def manage_friends():
    username = session["username"]
    if request.method == "GET":
        if "username" not in session:
            return render_template("friends.html")
        friend_requests = friends.show_friend_requests(username)
        all_friends = friends.show_friends(username)
        return render_template(
            "friends.html", friend_requests=friend_requests, all_friends=all_friends
        )

    if request.method == "POST":
        user_id_to_accept = request.form.get("user_id")
        friends.accept_friend_request(username, user_id_to_accept)
        return redirect("/profile/friends")


@app.route("/new_post", methods=["GET", "POST"])
def add_new_post():
    if "username" in session:
        username = session["username"]
        if request.method == "GET":
            min, max = lunch.max_week()
            return render_template("new_post.html", min_date=min, max_date=max)

        if request.method == "POST":
            lunch.create_lunch_post(username)
            return redirect("/posts")

        return render_template("new_post.html")

    error_message = "not_signed_in"
    return render_template("new_post.html", error=error_message)


@app.route("/posts", methods=["GET", "POST"])
def all_posts():
    access = False
    if "username" in session:
        all_posts = lunch.all_lunch_posts()
        access = True
        return render_template("posts.html", all_posts=all_posts, access=access)
    return render_template("posts.html", access=access)


@app.route("/posts/<int:id>", methods=["GET", "POST"])
def post(id):
    if request.method == "GET":
        access = False
        if "username" in session:
            data = lunch.one_post(id)
            current_user = session["username"]
            other_user = data[0]
            comments = lunch.show_comments(id)
            if (
                (friends.is_friend(current_user, other_user) and data[6] == "friends")
                or data[6] == "public"
                or data[0] == current_user
            ):
                access = True
                return render_template(
                    "post.html", data=data, access=access, comments=comments
                )
        return render_template("post.html", access=access)

    if request.method == "POST":
        data = lunch.one_post(id)
        lunch.comment_post(id)
        return redirect(url_for("post", id=id))
