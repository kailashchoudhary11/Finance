import requests
import os
import json
from urllib.parse import quote_plus
from django.shortcuts import render

def apology(request, message, code=400):
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
    return render(request, "home/apology.html", {"top" : code, "bottom":escape(message)})

def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = "pk_81fd8848db9e4f239d661690a2b11612"
        url = f"https://cloud.iexapis.com/stable/stock/{quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None

def usd(value):
    return f"${value:,.2f}"