from flask import Flask, render_template, request, redirect, session
import requests
from recommendation_engine import calculate_fair_price
from market_data import generate_recommendation

app = Flask(__name__)
app.secret_key = "smartbuy_secret"

API_KEY = "d4d9f5c2fdcb0e07d93f1caba178f234422e4e1cd21c01ff791d4cc21d9a88b5"

PRODUCT_CACHE = []


def fetch_products(query="laptop"):
    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    products = []

    for i, item in enumerate(data.get("shopping_results", [])):
        title = item.get("title", "").lower()
        price_text = item.get("price", "")

        if not price_text:
            continue

        clean_price = "".join(ch for ch in price_text if ch.isdigit())

        if not clean_price:
            continue

        price = int(clean_price)

        if price < 1000 or price > 500000:
            continue

        if "case" in title or "cover" in title or "charger" in title:
            continue

        products.append({
            "id": i,
            "Product_Name": item.get("title", "Unknown"),
            "Current_Price": price,
            "Image": item.get("thumbnail", ""),
            "Source": item.get("source", "")
        })

    return products


@app.route("/")
def home():
    global PRODUCT_CACHE

    query = request.args.get("search", "electronics")
    PRODUCT_CACHE = fetch_products(query)

    return render_template(
        "home.html",
        products=PRODUCT_CACHE,
        query=query
    )


@app.route("/product/<int:product_id>")
def product_page(product_id):
    global PRODUCT_CACHE

    if product_id >= len(PRODUCT_CACHE):
        return "Product not found"

    product = PRODUCT_CACHE[product_id]

    analysis = calculate_fair_price(product["Product_Name"])

    recommendation = generate_recommendation(
        product["Current_Price"],
        analysis["predicted_fair_price"]
    )

    return render_template(
        "product.html",
        product=product,
        current_price=product["Current_Price"],
        predicted_price=analysis["predicted_fair_price"],
        analysis=analysis,
        price_recommendation=recommendation,
        status=recommendation["status"]
    )


@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    global PRODUCT_CACHE

    cart = session.get("cart", [])

    product = PRODUCT_CACHE[product_id]

    # check if already exists
    for item in cart:
        if item["id"] == product_id:
            item["quantity"] += 1
            break
    else:
        cart.append({
            "id": product_id,
            "Product_Name": product["Product_Name"],
            "Current_Price": product["Current_Price"],
            "Image": product["Image"],
            "quantity": 1
        })

    session["cart"] = cart

    return redirect("/cart")


@app.route("/increase/<int:product_id>")
def increase(product_id):
    cart = session.get("cart", [])

    for item in cart:
        if item["id"] == product_id:
            item["quantity"] += 1

    session["cart"] = cart

    return redirect("/cart")


@app.route("/decrease/<int:product_id>")
def decrease(product_id):
    cart = session.get("cart", [])

    for item in cart:
        if item["id"] == product_id:
            item["quantity"] -= 1

            if item["quantity"] <= 0:
                cart.remove(item)

            break

    session["cart"] = cart

    return redirect("/cart")


@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])

    cart = [
        item for item in cart
        if item["id"] != product_id
    ]

    session["cart"] = cart

    return redirect("/cart")


@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])

    total = sum(
        item["Current_Price"] * item.get("quantity", 1)
        for item in cart_items
    )

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )


@app.route("/buy")
def buy():
    session["cart"] = []

    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
