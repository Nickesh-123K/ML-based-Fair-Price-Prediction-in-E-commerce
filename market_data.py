import requests

API_KEY = "d4d9f5c2fdcb0e07d93f1caba178f234422e4e1cd21c01ff791d4cc21d9a88b5"


def get_price_range_filter(product_name):
    name = product_name.lower()

    if "iphone" in name or "samsung" in name:
        return 20000, 300000

    if "laptop" in name:
        return 25000, 300000

    if "headphone" in name:
        return 500, 20000

    if "makeup" in name or "lipstick" in name:
        return 100, 5000

    return 0, 999999


def fetch_market_prices(product_name):
    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_shopping",
        "q": product_name,
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    prices = []

    min_p, max_p = get_price_range_filter(product_name)

    for item in data.get("shopping_results", []):
        price_text = item.get("price", "")

        if not price_text:
            continue

        clean_price = "".join(ch for ch in price_text if ch.isdigit())

        if not clean_price:
            continue

        price = int(clean_price)

        if price < min_p or price > max_p:
            continue

        prices.append(price)

    return prices


def get_market_summary(product_name):
    prices = fetch_market_prices(product_name)

    if not prices:
        return {
            "avg_price": 0,
            "min_price": 0,
            "max_price": 0,
            "median_price": 0
        }

    prices.sort()

    # Remove extreme outliers if enough data exists
    if len(prices) > 4:
        prices = prices[1:-1]

    n = len(prices)

    # Proper median calculation
    if n % 2 == 0:
        median_price = (prices[n // 2 - 1] + prices[n // 2]) / 2
    else:
        median_price = prices[n // 2]

    return {
        "avg_price": round(sum(prices) / n, 2),
        "min_price": min(prices),
        "max_price": max(prices),
        "median_price": round(median_price, 2)
    }


def generate_recommendation(current_price, fair_price):
    diff = ((current_price - fair_price) / fair_price) * 100

    if diff > 15:
        status = "OVERPRICED"
        advice = "Wait for price drop"

    elif diff < -10:
        status = "UNDERPRICED"
        advice = "Buy now"

    else:
        status = "FAIRLY PRICED"
        advice = "Reasonable purchase"

    return {
        "status": status,
        "difference_percent": round(diff, 2),
        "advice": advice
    }
