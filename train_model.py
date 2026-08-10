import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

#
# LOAD DATA
#
df = pd.read_csv("ecommerce_fair_price_dataset.csv")

#
# FIX PRICE SCALE (IMPORTANT)
#
df["Original_Price"] = df["Original_Price"] / 10
df["Current_Price"] = df["Current_Price"] / 10
df["Fair_Price"] = df["Fair_Price"] / 10

#
# ENCODING
#
category_encoder = LabelEncoder()
brand_encoder = LabelEncoder()

df["Category"] = category_encoder.fit_transform(df["Category"])
df["Brand"] = brand_encoder.fit_transform(df["Brand"])

#
# FEATURES
#
X = df[
    [
        "Category",
        "Brand",
        "Original_Price",
        "Discount_Percentage",
        "Seller_Rating",
        "Demand_Score",
        "Days_Since_Launch",
    ]
]

y = df["Fair_Price"]

#
# TRAIN MODEL
#
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    random_state=42
)

model.fit(X_train, y_train)

#
# EVALUATION
#
pred = model.predict(X_test)

mae = abs(y_test - pred).mean()
r2 = model.score(X_test, y_test)

print("MAE:", mae)
print("R2 Score:", r2)

#
# SAVE MODEL
#
pickle.dump(model, open("fair_price_model.pkl", "wb"))
pickle.dump(category_encoder, open("category_encoder.pkl", "wb"))
pickle.dump(brand_encoder, open("brand_encoder.pkl", "wb"))

print("MODEL TRAINED SUCCESSFULLY")
