import streamlit as st
import pandas as pd

st.set_page_config(page_title="Electronics Price Aggregator", layout="wide")

st.title("🔍 Electronics Price Aggregator")
st.write("Compare prices across Amazon, Flipkart, Croma & Reliance Digital")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    amazon1 = pd.read_csv("amazon1.csv")
    amazon2 = pd.read_csv("amazon2.csv")
    croma = pd.read_csv("croma.csv")
    flipkart_mobile = pd.read_csv("flipkart_mobile_data.csv")
    flipkart_laptops = pd.read_csv("flipkart_laptops.csv")
    flipkart_earphones = pd.read_csv("flipkart_earphones.csv")
    reliance = pd.read_csv("Reliance Digital India Product Dataset.csv")

    # ---------- STANDARDIZE ----------
    def clean(df, col_mapping, category, source):
        df_cleaned = df.rename(columns=col_mapping)

        # Ensure required columns are present, adding as pd.NA if missing
        for col in ["product_name", "price", "brand"]:
            if col not in df_cleaned.columns:
                df_cleaned[col] = pd.NA

        df_cleaned["category"] = category
        df_cleaned["source"] = source
        return df_cleaned[["product_name", "brand", "category", "price", "source"]]

    frames = [
        clean(amazon1, {"name": "product_name", "actual_price": "price"}, "Electronics", "Amazon"),
        clean(amazon2, {"name": "product_name", "actual_price": "price"}, "Electronics", "Amazon"),
        clean(flipkart_mobile, {"Title": "product_name", "Price": "price"}, "Mobile", "Flipkart"),
        clean(flipkart_laptops, {"Title": "product_name", "Price": "price"}, "Laptop", "Flipkart"),
        clean(flipkart_earphones, {"Title": "product_name", "Price": "price"}, "Earphones", "Flipkart"),
        clean(croma, {"name": "product_name", "price": "price"}, "Electronics", "Croma"),
        clean(reliance, {"Product Name": "product_name", "Price (₹)": "price", "Brand": "brand"}, "Electronics", "Reliance Digital")
    ]

    df = pd.concat(frames, ignore_index=True)

    # ---------- CLEAN ----------
    df["price"] = (
        df["price"].astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    df["product_name"] = df["product_name"].str.lower().str.strip()

    return df.dropna(subset=["price", "product_name"])

data = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔧 Filters")

category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(data["category"].unique().tolist())
)

brand = st.sidebar.selectbox(
    "Select Brand",
    ["All"] + sorted(data["brand"].dropna().unique().tolist())
)

# ---------------- FILTER DATA ----------------
filtered = data.copy()

if category != "All":
    filtered = filtered[filtered["category"] == category]

if brand != "All":
    filtered = filtered[filtered["brand"] == brand]

# ---------------- PRICE COMPARISON ----------------
comparison = filtered.loc[
    filtered.groupby("product_name")["price"].idxmin()
].sort_values("price")

# ---------------- SEARCH ----------------
search = st.text_input("🔎 Search Product")

if search:
    comparison = comparison[
        comparison["product_name"].str.contains(search.lower())
    ]

# ---------------- DISPLAY ----------------
st.subheader("💰 Best Price Available")

st.dataframe(
    comparison.rename(columns={
        "product_name": "Product",
        "brand": "Brand",
        "category": "Category",
        "price": "Price (₹)",
        "source": "Store"
    }),
    use_container_width=True
)

# ---------------- STATS ----------------
st.subheader("📊 Platform Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Products", len(comparison))
col2.metric("Lowest Price (₹)", int(comparison["price"].min()))
col3.metric("Highest Price (₹)", int(comparison["price"].max()))
