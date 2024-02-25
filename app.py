from sqlite3 import IntegrityError
from flask import Flask, request, url_for, redirect, render_template, session, flash
from datetime import timedelta, datetime
import base64
import utils, os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import db, validators
import datetime

# imported all necessacary  libraries in the above section

app = Flask(__name__)
app.secret_key = "findwhatyouloveandletitKILLYOU"
app.permanent_session_lifetime = timedelta(days=5)
connection = db.connect_to_database()
limiter = Limiter(
    app=app, key_func=get_remote_address, default_limits=["50 per minute"]
)
#created a instance and set the limiter
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
#app is configured with some extensions

@app.route("/", methods=["GET", "POST"])
def home():
    check_login = session.get("logged_in", False)
    check_register = session.get("registered", False)
    if check_login and check_register:
        if request.method == "POST":
            if "username" in request.form and request.form["username"]:
                userName = request.form["username"]
                user = db.get_user_with_posts(connection, userName)
                if not user:
                    flash("The user you search for does not exist !", "danger")
                    return redirect(url_for("home"))
                else:
                    return render_template("profile.html", user=user)
            elif "description" in request.form and request.form["description"]:
                image_for_post = request.files["image"]
                if not image_for_post or image_for_post.filename == "":
                    flash("Nothing was Selected, please Choose something", "danger")
                    return render_template("home.html")

                if not validators.allowed_file(
                    image_for_post.filename
                ) or not validators.allowed_file_size(image_for_post):
                    flash("Invalid File is Uploaded", "danger")
                    return render_template("home.html")
                description_for_post = request.form["description"]
                image_data = base64.b64encode(image_for_post.read()).decode("utf-8")
                image_ext = image_for_post.filename.split(".")[1]
                user_id = session["user_id"]
                db.add_post(
                    connection,
                    user_id,
                    description_for_post,
                    image_data,
                    image_ext,
                    datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                )
                flash("Post Created Successfully!!", "success")
            else:
                post_id = request.form["post_id"]
                db.delete_post_by_id(
                    connection,
                    post_id,
                )
        posts = db.get_all_posts(connection)
        return render_template("home.html", posts=posts)
    elif check_register and not check_login:
        flash("Please Log in First", "info")
        return redirect(url_for("login"))
    else:
        flash("Please Register First", "info")
        return redirect(url_for("register"))
    

# the above section is for home page and connect with the sqlite3 database


@app.route("/profile/<user_id>", methods=["GET", "POST"])
def profile(user_id):

    check_login = session.get("logged_in", False)
    check_register = session.get("registered", False)
    if check_register and not check_login:
        return redirect(url_for("login"))
    elif not check_register and not check_login:
        return redirect(url_for("register"))
    else :
        username = db.get_user_by_user_id(connection, user_id)[1]
        user = db.get_user_with_posts(connection, username)
        return render_template("profile.html", user=user)

# in the above section it calls the user where he  get the posts what he shared .

@app.route("/display_post/<post_id>", methods=["GET", "POST"])
def display_post(post_id):
    check_login = session.get("logged_in", False)
    check_register = session.get("registered", False)
    if check_register and not check_login:
        return redirect(url_for("login"))
    elif not check_register and not check_login:
        return redirect(url_for("register"))
    post = db.get_post_by_post_id(connection, post_id)
    print(post_id)
    comments = db.get_comments_by_post_id(connection, post_id)
    if request.method == "GET":
        return render_template("display_post.html", post=post, comments=comments)
    elif request.method == "POST":
        user_id = session["user_id"]
        if "comment" in request.form and request.form["comment"]:
            comment_content = request.form["comment"]
            db.add_comment_to_db(
                connection,
                user_id,
                comment_content,
                post_id,
                datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
            )
        else:
            comment_id = request.form["comment_id"]
            db.delete_comment_by_id(
                connection,
                comment_id,
            )
    return redirect(url_for("display_post", post_id=post_id))

# the above code is posting the posts in the Feed,including the time stamp also(Date and Time they posted the post)



@app.route("/register", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        dob=request.form["dob"]
        profile_photo=request.files["profile_photo"]
        if not utils.is_strong_password(password):
            flash(
                "Sorry You Entered a weak Password Please Choose a stronger one",
                "danger",
            )
            return render_template("register.html")

        token = db.get_user_by_username(connection, username)

        if not token:
            hashedPassword = utils.hash_password(password)

            if profile_photo.filename:
                profile_photo_data = profile_photo.read()
            else:
                profile_photo_data = None
            
            db.add_user(
                connection, username, hashedPassword,dob, profile_photo_data
            )  # if username in database already in database it will return an error to terminate the server
            session["username"] = username
            session["logged_in"] = False
            session["registered"] = True
            session["user_id"] = db.get_user_by_username(connection, username)[0]
            flash("Account Created Successfully!!", "success")
            return redirect(url_for("login"))
        else:
            flash("User already exists!", "danger")
            session["registered"] = True
            return redirect(url_for("login"))

    return render_template("register.html")

# the above section is used for the register page where the user can register using their username,password,dob,profile_photo.

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.get_user_by_username(connection, username)
        if user:
            real_password = user[2]
            if utils.is_password_match(password, real_password):
                session["logged_in"] = True
                session["username"] = username
                session["user_id"] = user[0]
                session["admin"] = user[3]
                flash("Welcome " + username, "success")
                return redirect(url_for("home"))
            else:
                flash("Incorrect Password. Please try again.", "danger")
        else:
            flash("User does not exist. Please register!", "danger")
            return redirect(url_for("register"))
    return render_template("login.html")

# the above code is used for login to check the user typed the user name and the password


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("logged_in", None)
    flash("Logged Out Successfully!", "success")
    return redirect(url_for("login"))

#the above code is used for the logout section

@app.route("/allusers")
def all_users():
    if session.get("logged_in"):
        users = db.get_all_users(connection)
        user_id = db.get_all_userid(connection)
        return render_template("allusers.html", users=users,user_id=user_id)
    else:
        flash("Please log in to access this page.", "info")
        return redirect(url_for("login"))
    
#the above code is used for getting all users who all are using the app


if __name__ == "__main__":
    db.init_users(connection)
    db.init_posts(connection)
    db.init_comments(connection)
    app.run(debug=True)
    # initialize the comments and run the program.
