import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import io
import uuid
import pandas as pd
import matplotlib.pyplot as plt
from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code



def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history&includeAdjustedClose=true"
    )

    # Query API
    try:
        response = requests.get(url, cookies={"session": str(uuid.uuid4())}, headers={"User-Agent": "python-requests", "Accept": "*/*"})
        response.raise_for_status()

        # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
        quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
        quotes.reverse()
        price = round(float(quotes[0]["Adj Close"]), 2)

        # Extract dates and closing prices for graphs
        dates = [quote["Date"] for quote in quotes]
        closing_prices = [float(quote["Adj Close"]) for quote in quotes]

        # Display the graph
        plt.figure(figsize=(12, 6))
        plt.plot(dates, closing_prices, label=f'{symbol} Closing Price', color='blue')
        plt.xlabel('Date')
        plt.ylabel("Closing Price")
        plt.title(f'{symbol} Stock Price from {start} to {end}')
        plt.legend()
        plt.grid(True)
        plt.show()

        return {
            "name": symbol,
            "price": price,
            "symbol": symbol,
            "graph_generated": True,  # Added missing comma here
        }
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None

def generate_stock_graph(stock_data, symbol):
    """Generate and save the stock price graph using Matplotlib."""

    # Check if 'historical_data' is present in stock_data
    if 'historical_data' not in stock_data:
        return None  # Return None if historical data is missing

    dates = stock_data["historical_data"]["Date"]
    closing_prices = stock_data["historical_data"]["Adj Close"]

    # Create the graph
    plt.figure(figsize=(12, 6))
    plt.plot(dates, closing_prices, label=f'{symbol} Closing Price', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title(f'{symbol} Stock Price')
    plt.legend()
    plt.grid(True)

    # Save the graph as an image in memory
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    # Clear the Matplotlib plot to free up resources
    plt.clf()

    return img_buffer


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
