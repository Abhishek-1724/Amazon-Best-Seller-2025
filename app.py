import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Amazon_bestsellers_items_2025.csv")
    
    # Convert datatypes
    df['product_price'] = pd.to_numeric(df['product_price'], errors='coerce')
    df['product_star_rating'] = pd.to_numeric(df['product_star_rating'], errors='coerce')
    df['product_num_ratings'] = (
        df['product_num_ratings']
        .astype(str)
        .str.replace(',', '', regex=False)
        .astype(float)
    )
    
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filters")
country_filter = st.sidebar.multiselect("Select Country:", df['country'].unique())
if country_filter:
    df = df[df['country'].isin(country_filter)]

# --- Dashboard Title ---
st.title("📊 Amazon Product Dashboard")

# --- Overview ---
st.subheader("Dataset Overview")
st.write(df.head())

# --- Price Distribution ---
st.subheader("Distribution of Product Prices")
fig, ax = plt.subplots(figsize=(8,5))
df['product_price'].hist(bins=50, ax=ax)
ax.set_xlabel("Product Price")
ax.set_ylabel("Count")
st.pyplot(fig)

# --- Rating Distribution ---
st.subheader("Distribution of Star Ratings")
fig, ax = plt.subplots(figsize=(6,4))
df['product_star_rating'].hist(bins=20, ax=ax)
ax.set_xlabel("Star Rating")
ax.set_ylabel("Count")
st.pyplot(fig)

# --- Top 10 Products by Number of Ratings ---
st.subheader("Top 10 Most Rated Products")
top_products = df.sort_values('product_num_ratings', ascending=False).head(10)
st.table(top_products[['product_title', 'product_num_ratings']])

# --- Correlation Heatmap ---
st.subheader("Correlation between Price, Rating, and Num of Ratings")
fig, ax = plt.subplots(figsize=(6,4))
sns.heatmap(df[['product_price','product_star_rating','product_num_ratings']].corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)
