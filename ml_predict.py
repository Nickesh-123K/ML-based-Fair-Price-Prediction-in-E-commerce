import pickle
import pandas as pd

model = pickle.load(open("fair_price_model.pkl", "rb"))
category_encoder = pickle.load(open("category_encoder.pkl", "rb"))
brand_encoder = pickle.load(open("brand_encoder.pkl", "rb"))


def predict_fair_price(product_data):
    try:
        category = category_encoder.transform(
            [product_data["Category"]]
        )[0]

        brand = brand_encoder.transform(
            [product_data["Brand"]]
        )[0]

    except:
        category = 0
        brand = 0

    input_df = pd.DataFrame([
        {
            "Category": category,
            "Brand": brand,
            "Original_Price": product_data["Original_Price"],
            "Discount_Percentage": product_data["Discount_Percentage"],
            "Seller_Rating": product_data["Seller_Rating"],
            "Demand_Score": product_data["Demand_Score"],
            "Days_Since_Launch": product_data["Days_Since_Launch"]
        }
    ])

    prediction = model.predict(input_df)[0]

    return round(prediction, 2)
