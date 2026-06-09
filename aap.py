import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Snapdeal Product Scraper", layout="wide")

st.title("🛒 Snapdeal Product Scraper")

keyword = st.text_input("Enter Product Keyword", "mobile")

if st.button("Scrape Products"):

    url = f"https://www.snapdeal.com/search?keyword={keyword}"

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            st.error("Failed to fetch data.")
            st.stop()

        soup = BeautifulSoup(response.text, "lxml")

        products = soup.find_all("div", class_="product-tuple-listing")

        data = []

        for product in products:

            try:
                name = product.find(
                    "p",
                    class_="product-title"
                ).get_text(strip=True)

            except:
                name = "N/A"

            try:
                price = product.find(
                    "span",
                    class_="lfloat product-price"
                )["data-price"]

            except:
                price = "N/A"

            try:
                old_price = product.find(
                    "span",
                    class_="lfloat product-desc-price strike"
                ).text.strip()

            except:
                old_price = "N/A"

            try:
                discount = product.find(
                    "div",
                    class_="product-discount"
                ).text.strip()

            except:
                discount = "N/A"

            try:
                rating = product.find(
                    "div",
                    class_="filled-stars"
                )["style"]

            except:
                rating = "N/A"

            try:
                reviews = product.find(
                    "p",
                    class_="product-rating-count"
                ).text.strip()

            except:
                reviews = "N/A"

            data.append({
                "Product Name": name,
                "Original Price": old_price,
                "Discounted Price": price,
                "Discount %": discount,
                "Rating": rating,
                "Reviews": reviews
            })

        df = pd.DataFrame(data)

        st.success(f"Found {len(df)} Products")

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{keyword}_products.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error: {e}")



