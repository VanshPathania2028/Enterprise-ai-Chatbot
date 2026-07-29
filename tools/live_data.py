"""Live weather and stock-data helpers used by API routes and chat."""

import re
from datetime import datetime

import requests

from config import STOCK_API_KEY


WEATHER_CODES = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "rime fog",
    51: "light drizzle",
    53: "drizzle",
    55: "heavy drizzle",
    61: "light rain",
    63: "rain",
    65: "heavy rain",
    71: "light snow",
    73: "snow",
    75: "heavy snow",
    80: "rain showers",
    81: "rain showers",
    82: "heavy rain showers",
    95: "thunderstorm",
}

NON_SYMBOL_WORDS = {
    "a",
    "an",
    "the",
    "my",
    "today",
    "current",
    "latest",
    "give",
    "tell",
    "what",
}


def get_weather(city: str) -> dict:
    """Return the current weather for a city using Open-Meteo."""
    location = city.strip()
    if not location:
        raise ValueError("Provide a city, for example: weather in Delhi.")

    geocoding_response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": location, "count": 1, "language": "en"},
        timeout=10,
    )
    geocoding_response.raise_for_status()
    results = geocoding_response.json().get("results", [])

    if not results:
        raise LookupError(f"I could not find a location named '{location}'.")

    place = results[0]
    weather_response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": "temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": "auto",
        },
        timeout=10,
    )
    weather_response.raise_for_status()
    current = weather_response.json()["current"]
    description = WEATHER_CODES.get(
        current.get("weather_code"), "unknown conditions"
    )
    place_name = ", ".join(
        part
        for part in (place.get("name"), place.get("country"))
        if part
    )

    return {
        "source": "Open-Meteo",
        "location": place_name,
        "temperature_c": current.get("temperature_2m"),
        "feels_like_c": current.get("apparent_temperature"),
        "humidity_percent": current.get("relative_humidity_2m"),
        "wind_speed_kmh": current.get("wind_speed_10m"),
        "condition": description,
        "observed_at": current.get("time"),
    }


def get_stock_quote(symbol: str) -> dict:
    """Return a latest available quote from Alpha Vantage."""
    if not STOCK_API_KEY:
        raise RuntimeError("Stock data is not configured. Set STOCK_API_KEY in .env.")

    normalized_symbol = symbol.strip().upper()
    if not re.fullmatch(r"[A-Z0-9.-]{1,15}", normalized_symbol):
        raise ValueError("Provide a valid stock symbol, for example: AAPL.")

    response = requests.get(
        "https://www.alphavantage.co/query",
        params={
            "function": "GLOBAL_QUOTE",
            "symbol": normalized_symbol,
            "apikey": STOCK_API_KEY,
        },
        timeout=15,
    )
    response.raise_for_status()
    payload = response.json()

    if "Note" in payload:
        raise RuntimeError("The stock-data provider rate limit was reached. Try again shortly.")
    if "Error Message" in payload:
        raise LookupError(f"No quote was found for {normalized_symbol}.")

    quote = payload.get("Global Quote", {})
    price = quote.get("05. price")
    if not price:
        raise LookupError(f"No current quote was found for {normalized_symbol}.")

    return {
        "source": "Alpha Vantage",
        "symbol": quote.get("01. symbol", normalized_symbol),
        "price": float(price),
        "change": float(quote.get("09. change", 0)),
        "change_percent": quote.get("10. change percent", "0%"),
        "latest_trading_day": quote.get("07. latest trading day"),
        "retrieved_at": datetime.now().astimezone().isoformat(),
    }


def live_chat_response(message: str) -> str | None:
    """Return a live-data answer for an explicitly weather or stock query."""
    normalized_message = message.strip()
    lower_message = normalized_message.lower()

    if "weather" in lower_message:
        city_match = re.search(r"\b(?:in|for|at)\s+([\w .,'-]+?)(?:[?!.]|$)", normalized_message, re.I)
        if not city_match:
            city_match = re.search(
                r"\bweather\s+(?:today\s+|now\s+|currently\s+)?([A-Za-z][\w .,'-]*?)(?:[?!.]|$)",
                normalized_message,
                re.I,
            )
        if not city_match:
            city_match = re.search(
                r"\b([A-Za-z][\w .,'-]*?)\s+weather\b",
                normalized_message,
                re.I,
            )
        if not city_match:
            return "Please include a city, for example: What is the weather in Delhi?"

        city = city_match.group(1).strip()
        if city.lower() in {"the", "today", "now", "current", "currently"}:
            return "Please include a city, for example: What is the weather in Delhi?"

        weather = get_weather(city)
        return (
            f"Current weather in {weather['location']}: {weather['condition']}, "
            f"{weather['temperature_c']}°C (feels like {weather['feels_like_c']}°C), "
            f"humidity {weather['humidity_percent']}%, and wind {weather['wind_speed_kmh']} km/h. "
            f"Source: {weather['source']} at {weather['observed_at']}."
        )

    stock_match = re.search(
        r"\b(?:stock price|stock quote|share price|quote|price)\s+(?:of|for)?\s*([A-Za-z0-9.-]{1,15})\b",
        normalized_message,
        re.I,
    )
    if not stock_match:
        stock_match = re.search(
            r"\b([A-Za-z0-9.-]{1,15})\s+(?:stock price|stock quote|share price)\b",
            normalized_message,
            re.I,
        )
    if stock_match:
        symbol = stock_match.group(1)
        if symbol.lower() in NON_SYMBOL_WORDS:
            return "Please include a stock symbol, for example: What is the AAPL stock price?"

        quote = get_stock_quote(symbol)
        return (
            f"Latest available quote for {quote['symbol']}: ${quote['price']:.2f} "
            f"({quote['change']:+.2f}, {quote['change_percent']}) on {quote['latest_trading_day']}. "
            f"Source: {quote['source']}. This is informational, not investment advice."
        )

    if any(term in lower_message for term in ("stock", "share price", "stock price")):
        return "Please include a stock symbol, for example: What is the AAPL stock price?"

    return None
