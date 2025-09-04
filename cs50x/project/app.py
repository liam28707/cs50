import os
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from function import apology, login_required, generate_random_password

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///passbank.db")


@app.after_request
def after_request(response):
    # Makes sure responses aren't cached#
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return apology("Must provide username", 403)
        elif not password:
            return apology("Must provide password", 403)
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        confirmation = request.form["confirmation"]

        if not re.match(r"^[\w\.-]+@[\w\.-]+(\.[\w]+)+$", email):
            return apology("invalid email format", 400)

        user = db.execute("SELECT username, email FROM users")
        exis_usernames = [u["username"] for u in user]
        exis_emails = [u["email"] for u in user]

        if not username:
            return apology("missing username", 400)
        if not email:
            return apology("missing email", 400)
        elif username in exis_usernames:
            return apology("username already taken", 400)
        elif email in exis_emails:
            return apology("email already used", 400)
        elif not password or not confirmation:
            return apology("missing password", 400)
        elif password != confirmation:
            return apology("passwords don't match", 400)

        psw = generate_password_hash(password)
        db.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            username,
            psw,
            email,
        )
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/change_pass", methods=["GET", "POST"])
def change_pass():
    if request.method == "POST":
        email = request.form["email"]
        current_pass = request.form["current_pass"]
        new_pass = request.form["new_pass"]
        confirmation = request.form["confirmation"]

        users = db.execute("SELECT * FROM users WHERE email = ?", email)

        if not users:
            flash("User not found", "error")
            return redirect("/change_pass")

        user = users[0]  # Access the first user row

        if not check_password_hash(user["password"], current_pass):
            flash("Current password is incorrect", "error")
            return redirect("/change_pass")

        if new_pass != confirmation:
            flash("Passwords don't match", "error")
            return redirect("/change_pass")

        new_password_hash = generate_password_hash(new_pass)
        db.execute(
            "UPDATE users SET password = ? WHERE email = ?", new_password_hash, email
        )

        flash("Password changed successfully!", "success")
        return redirect("/")
    else:
        return render_template("change_pass.html")  # Replace with your template name


@app.route("/passbank", methods=["GET", "POST"])
@login_required
def passbank():
    if request.method == "POST":
        website_name = request.form.get("website_name")
        username = request.form.get("username")
        password = request.form.get("password")

        db.execute(
            "INSERT INTO PasswordBank (user_id, website_name, username, password) VALUES (?, ?, ?, ?)",
            session["user_id"],
            website_name,
            username,
            password,
        )

        flash("Password added Successfully")
        return redirect("/passbank")

    elif request.method == "GET":
        passwords = db.execute(
            "SELECT * FROM PasswordBank WHERE user_id = ?", session["user_id"]
        )
        return render_template("passbank.html", passwords=passwords)


@app.route("/passbank/add", methods=["GET", "POST"])
@login_required
def add_password():
    if request.method == "POST":
        website_name = request.form.get("website_name")
        username = request.form.get("username")
        password = request.form.get("password")

        db.execute(
            "INSERT INTO PasswordBank (user_id, website_name,username,password) VALUES (?,?,?,?)",
            session["user_id"],
            website_name,
            username,
            password,
        )

        flash("Password added Successfully")
        return redirect("/passbank")

    return render_template("addpass.html")


@app.route("/passbank/edit/<int:password_id>", methods=["GET", "POST"])
@login_required
def edit_password(password_id):
    if request.method == "POST":
        # Handle form submission and update the password entry in the database
        website_name = request.form.get("website_name")
        username = request.form.get("username")
        new_password = request.form.get("new_password")

        # Update the password entry in the database
        db.execute(
            "UPDATE PasswordBank SET website_name = ?, username = ?, password = ? WHERE id = ?",
            website_name,
            username,
            new_password,
            password_id,
        )

        flash("Password updated successfully")
        return redirect("/passbank")
    else:
        # Fetch the password details from the database based on the password_id
        password = db.execute("SELECT * FROM PasswordBank WHERE id = ?", password_id)

        if not password:
            # Handle the case where the password entry doesn't exist
            return apology("Password not found", 404)

        return render_template("edit_password.html", password=password[0])


@app.route("/passbank/delete/<int:password_id>")
@login_required
def delete_password(password_id):
    db.execute("DELETE FROM PasswordBank WHERE id = ?", password_id)

    flash("Password deleted Successfully")
    return redirect("/passbank")


@app.route("/passgenerator")
@login_required
def password_generator():
    return render_template("password_generator.html")


@app.route("/generate_password", methods=["GET", "POST"])
@login_required
def generate_password():
    if request.method == "POST":
        length = int(
            request.json.get("length", 12)
        )  # Get length from request, default to 12 if not provided
        generated_password = generate_random_password(length)
        return jsonify(generated_password)
    elif request.method == "GET":
        return render_template("password_generator.html")
