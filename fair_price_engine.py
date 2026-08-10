from market_data import get_market_summary

def calculate_fair_price(product_name, ml_prediction, historical_avg):
    market = get_market_summary(product_name)
    market_avg = market["median_price"]

    if market_avg == 0:
        fair_price = ml_prediction
    else:
        fair_price = (0.9 * market_avg) + (0.2 * ml_prediction)

    price_spread = market["max_price"] - market["min_price"]

    if market_avg > 0 and price_spread > market_avg * 0.5:
        confidence = "Low"
    else:
        confidence = "High"

    return {
        "predicted_fair_price": round(fair_price, 2),
        "market_avg": round(market_avg, 2),
        "market_min": market["min_price"],
        "market_max": market["max_price"],
        "confidence": confidence
    }

    return {
        "predicted_fair_price": round(final_price, 2),
        "market_avg": market_avg,
        "market_min": market["min_price"],
        "market_max": market["max_price"]
    }
