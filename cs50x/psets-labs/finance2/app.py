import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_cash = db.execute(
        "SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"]
    )[0]["cash"]
    portfolio = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
        user_id=session["user_id"],
    )
    total_portfolio_value = user_cash
    for stock in portfolio:
        symbol = stock["symbol"]
        total_shares = stock["total_shares"]
        stock_data = lookup(symbol)
        price = stock_data["price"]
        total_value = price * total_shares
        total_portfolio_value += total_value
        stock["price"] = price
        stock["total_value"] = total_value

    return render_template(
        "portfolio.html",
        portfolio=portfolio,
        user_cash=user_cash,
        total_portfolio_value=total_portfolio_value,
        usd=usd,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form["symbol"]
        symbols = lookup(symbol)
        shares_input = request.form["shares"]

        try:
            shares = int(shares_input)
            if shares <= 0:
                return apology("invalid shares", 400)
        except ValueError:
            return apology("invalid shares input", 400)

        if symbols is None:
            return apology("missing or invalid symbol", 400)

        share_price = symbols["price"]
        total_cost = share_price * shares
        user_cash = db.execute(
            "SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"]
        )[0]["cash"]
        if user_cash < total_cost:
            return apology("insufficient funds", 400)
        updated_cash = user_cash - total_cost
        db.execute(
            "UPDATE users SET cash = :updated_cash WHERE id = :user_id",
            updated_cash=updated_cash,
            user_id=session["user_id"],
        )

        db.execute(
            "INSERT INTO transactions(user_id, symbol, shares, price) VALUES(:user_id, :symbol, :shares, :price)",
            user_id=session["user_id"],
            symbol=symbol,
            shares=shares,
            price=share_price,
        )
        return redirect("/")
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = :user_id ORDER BY timestamp DESC",
        user_id=session["user_id"],
    )
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form["symbol"]
        symbols = lookup(symbol)
        if symbols is None:
            return apology("invalid symbol", 400)
        return render_template("quoted.html", symbol=symbols, usd=usd)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirmation = request.form["confirmation"]
        user = db.execute("SELECT username FROM users")
        exis_user = [u["username"] for u in user]
        if not username:
            return apology("missing username", 400)
        elif username in exis_user:
            return apology("username already taken", 400)
        elif not password or not confirmation:
            return apology("missing password", 400)
        elif password != confirmation:
            return apology("passwords don't match", 400)
        psw = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, psw)
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form["symbol"]
        shares = int(request.form["shares"])

        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol", 400)

        user_shares = db.execute(
            "SELECT SUM(shares) FROM transactions WHERE user_id = :user_id AND symbol = :symbol",
            user_id=session["user_id"],
            symbol=symbol,
        )[0]["SUM(shares)"]

        if user_shares is None or user_shares < shares:
            return apology("insufficient shares", 400)

        share_price = stock["price"]
        total_value = share_price * shares

        db.execute(
            "UPDATE users SET cash = cash + :total_value WHERE id = :user_id",
            total_value=total_value,
            user_id=session["user_id"],
        )

        db.execute(
            "INSERT INTO transactions (user_id,symbol,shares,price) VALUES (:user_id,:symbol,:shares, :price)",
            user_id=session["user_id"],
            symbol=symbol,
            shares=-shares,
            price=share_price,
        )

        return redirect("/")
    portfolio = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
        user_id=session["user_id"],
    )
    return render_template("sell.html", portfolio=portfolio)


@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    if request.method == "POST":
        deposit = float(request.form["deposit"])
        if deposit <= 0:
            return apology("invalid amount", 400)
        user = db.execute(
            "SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"]
        )
        if len(user) != 1:
            return apology("user not found", 403)
        current_cash = user[0]["cash"]
        updated_cash = current_cash + deposit

        db.execute(
            "UPDATE users SET cash = :updated_cash WHERE id = :user_id",
            updated_cash=updated_cash,
            user_id=user_id,
        )

        db.execute(
            "INSERT INTO transaction (user_id,symbol,shares,price) VALUE(:user_id, :symbol, :shares, :price)",
            user_id=user_id,
            symbol="DEPOSIT",
            shares=0,
            price=deposit,
        )
        flash("Deposit successful!")
    return render_template(
        "deposit.html",
    )
