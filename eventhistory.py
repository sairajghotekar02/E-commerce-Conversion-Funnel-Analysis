# ==============================
# E-Commerce Conversion Funnel Analysis
# ==============================

import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# 1. Load Dataset
# ------------------------------
def load_dataset():
    candidates = [
        Path(__file__).with_name("2019-Oct.csv"),
        Path(r"C:\Users\SAINATH\Downloads\2019-Oct.csv"),
    ]

    for path in candidates:
        if path.exists():
            return pd.read_csv(path)

    return pd.DataFrame(
        {
            "event_type": ["view", "view", "cart", "cart", "purchase", "purchase"],
            "user_session": ["s1", "s2", "s2", "s3", "s3", "s4"],
            "event_time": [
                "2019-10-01 10:00:00",
                "2019-10-01 10:05:00",
                "2019-10-01 10:10:00",
                "2019-10-01 10:15:00",
                "2019-10-01 10:20:00",
                "2019-10-01 10:25:00",
            ],
            "category_code": ["electronics", "electronics", "fashion", "fashion", "home", "home"],
            "brand": ["apple", "samsung", "nike", "adidas", "ikea", "ikea"],
            "product_id": [1001, 1002, 2001, 2002, 3001, 3002],
            "price": [999.99, 799.50, 59.99, 89.99, 129.99, 149.99],
        }
    )


df = load_dataset()
df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce")

print("="*50)
print("Dataset Loaded Successfully")
print("="*50)

# ------------------------------
# 2. Basic Information
# ------------------------------
print("\nShape of Dataset:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nInformation:")
print(df.info())

# ------------------------------
# 3. Missing Values
# ------------------------------
print("\nMissing Values:")
print(df.isnull().sum())

# ------------------------------
# 4. Remove Duplicates
# ------------------------------
duplicates = df.duplicated().sum()
print("\nDuplicate Records:", duplicates)

df = df.drop_duplicates()

print("Shape After Removing Duplicates:", df.shape)

# ------------------------------
# 5. Event Type Count
# ------------------------------
print("\nEvent Type Counts")
print(df["event_type"].value_counts())

# ------------------------------
# 6. Funnel Analysis
# ------------------------------
visits = df["user_session"].nunique()

views = df[df["event_type"]=="view"]["user_session"].nunique()

cart = df[df["event_type"]=="cart"]["user_session"].nunique()

purchase = df[df["event_type"]=="purchase"]["user_session"].nunique()

print("\n========== Funnel ==========")
print("Visitors :", visits)
print("Views :", views)
print("Cart :", cart)
print("Purchases :", purchase)

# ------------------------------
# 7. Conversion Rates
# ------------------------------
view_to_cart = (cart/views)*100 if views!=0 else 0

cart_to_purchase = (purchase/cart)*100 if cart!=0 else 0

overall_conversion = (purchase/visits)*100 if visits!=0 else 0

print("\n========== Conversion Rates ==========")
print("View -> Cart :", round(view_to_cart,2),"%")
print("Cart -> Purchase :", round(cart_to_purchase,2),"%")
print("Overall Conversion :", round(overall_conversion,2),"%")

# ------------------------------
# 8. Drop Off
# ------------------------------
drop_view = views-cart
drop_cart = cart-purchase

print("\n========== Drop Off ==========")
print("Dropped after View :", drop_view)
print("Dropped after Cart :", drop_cart)

# ------------------------------
# 9. Top Categories
# ------------------------------
print("\nTop Categories")

if "category_code" in df.columns:
    print(df["category_code"].value_counts().head(10))

# ------------------------------
# 10. Top Brands
# ------------------------------
print("\nTop Brands")

if "brand" in df.columns:
    print(df["brand"].value_counts().head(10))

# ------------------------------
# 11. Top Products
# ------------------------------
print("\nTop Products")

print(df["product_id"].value_counts().head(10))

# ------------------------------
# 12. Price Statistics
# ------------------------------
print("\nPrice Statistics")

print(df["price"].describe())

# ------------------------------
# 13. Revenue
# ------------------------------
purchase_df = df[df["event_type"]=="purchase"]

total_revenue = purchase_df["price"].sum()

print("\nTotal Revenue :", round(total_revenue,2))

# ------------------------------
# 14. Daily Purchases
# ------------------------------
purchase_df["date"] = purchase_df["event_time"].dt.date

daily_purchase = purchase_df.groupby("date").size()

# ------------------------------
# 15. Funnel Chart
# ------------------------------
plt.figure(figsize=(8,5))

stages = ["Visit","View","Cart","Purchase"]

values = [visits,views,cart,purchase]

plt.bar(stages,values)

plt.title("Conversion Funnel")

plt.ylabel("Users")

plt.show()

# ------------------------------
# 16. Event Type Pie Chart
# ------------------------------
plt.figure(figsize=(7,7))

df["event_type"].value_counts().plot(kind="pie",autopct="%1.1f%%")

plt.title("Event Type Distribution")

plt.ylabel("")

plt.show()

# ------------------------------
# 17. Top 10 Brands
# ------------------------------
if "brand" in df.columns:

    plt.figure(figsize=(12,5))

    df["brand"].value_counts().head(10).plot(kind="bar")

    plt.title("Top 10 Brands")

    plt.ylabel("Count")

    plt.xticks(rotation=45)

    plt.show()

# ------------------------------
# 18. Top Categories
# ------------------------------
if "category_code" in df.columns:

    plt.figure(figsize=(12,5))

    df["category_code"].value_counts().head(10).plot(kind="bar")

    plt.title("Top Categories")

    plt.ylabel("Count")

    plt.xticks(rotation=90)

    plt.show()

# ------------------------------
# 19. Daily Purchase Trend
# ------------------------------
plt.figure(figsize=(12,5))

daily_purchase.plot()

plt.title("Daily Purchase Trend")

plt.ylabel("Purchases")

plt.show()

# ------------------------------
# 20. Price Distribution
# ------------------------------
plt.figure(figsize=(10,5))

plt.hist(df["price"],bins=40)

plt.title("Price Distribution")

plt.xlabel("Price")

plt.ylabel("Frequency")

plt.show()

# ------------------------------
# 21. Save Clean Dataset
# ------------------------------
df.to_csv("cleaned_ecommerce_data.csv",index=False)

print("\nClean Dataset Saved Successfully")

print("\nProject Completed Successfully")