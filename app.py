import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Electronics Price Aggregator",
    layout="wide"
)

st.title("🔍 Electronics Price Aggregator")
st.write("Compare prices across Amazon, Flipkart, Croma & Reliance Digital")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():

    def safe_read(file):
        return pd.read_csv(
            file,
            encoding="latin-1",
            engine="python",
            on_bad_lines="skip"
        )

    amazon1 = safe_read("amazon1.csv")
    amazon2 = safe_read("amazon2.csv")
    croma = safe_read("croma.csv")
    flipkart_mobile = safe_read("flipkart_mobile_data.csv")
    flipkart_laptops = safe_read("flipkart_laptops.csv")
    flipkart_earphones = safe_read("flipkart_earphones.csv")
    reliance = safe_read("Reliance Digital India Product Dataset.csv")

    # -------- SAFE CLEAN FUNCTION --------
    def clean(df, col_map, category, source):
        df = df.rename(columns=col_map)

        # Ensure required columns always exist
        for col in ["product_name", "price", "brand"]:
            if col not in df.columns:
                df[col] = pd.NA

        df["category"] = category
        df["source"] = source

        return df[["product_name", "brand", "category", "price", "source"]]

    frames = [
        clean(amazon1, {"Product Name": "product_name", "Price": "price", "Brand": "brand"}, "Electronics", "Amazon"),
        clean(amazon2, {"Product Name": "product_name", "Price": "price", "Brand": "brand"}, "Electronics", "Amazon"),
        clean(flipkart_mobile, {"Product": "product_name", "Selling Price": "price", "Brand": "brand"}, "Mobile", "Flipkart"),
        clean(flipkart_laptops, {"Product": "product_name", "Selling Price": "price", "Brand": "brand"}, "Laptop", "Flipkart"),
        clean(flipkart_earphones, {"Product": "product_name", "Selling Price": "price", "Brand": "brand"}, "Earphones", "Flipkart"),
        clean(croma, {"Product Name": "product_name", "Price": "price", "Brand": "brand"}, "Electronics", "Croma"),
        clean(reliance, {"Product Name": "product_name", "Price": "price", "Brand": "brand"}, "Electronics", "Reliance Digital"),
    ]

    df = pd.concat(frames, ignore_index=True)

    # -------- CLEAN PRICE --------
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # -------- CLEAN PRODUCT NAME --------
    df["product_name"] = df["product_name"].astype(str).str.lower().str.strip()

    return df.dropna(subset=["product_name", "price"])

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
        comparison["product_name"].str.contains(search.lower(), na=False)
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

if not comparison.empty:
    col2.metric("Lowest Price (₹)", int(comparison["price"].min()))
    col3.metric("Highest Price (₹)", int(comparison["price"].max()))
else:
    col2.metric("Lowest Price (₹)", "N/A")
    col3.metric("Highest Price (₹)", "N/A")
