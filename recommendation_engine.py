from market_data import get_market_summary


def calculate_fair_price(product_name):
    market = get_market_summary(product_name)

    if market["avg_price"] == 0:
        fair_price = 0

    else:
        # Strong logic based only on live market
        fair_price = (
            0.5 * market["median_price"]
            + 0.3 * market["avg_price"]
            + 0.2 * market["min_price"]
        )

    return {
        "predicted_fair_price": round(fair_price, 2),
        "market_avg": market["avg_price"],
        "market_min": market["min_price"],
        "market_max": market["max_price"],
        "market_median": market["median_price"]
    }
