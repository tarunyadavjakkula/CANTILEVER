"""
Data analysis, processing, and data cleaning module for e-commerce products.
"""
import re
import pandas as pd
import numpy as np

# Rating word-to-number mapping
RATING_MAP = {
    "zero": 0.0,
    "one": 1.0,
    "two": 2.0,
    "three": 3.0,
    "four": 4.0,
    "five": 5.0
}

def clean_price(price):
    """
    Clean price values by stripping currency symbols ($ £ €),
    commas, and whitespace, returning a float.
    """
    if pd.isna(price) or price is None:
        return np.nan
    
    if isinstance(price, (int, float)):
        return float(price)

    price_str = str(price).strip()
    # Remove currency symbols ($ £ €) and commas
    cleaned = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(cleaned) if cleaned else np.nan
    except ValueError:
        return np.nan

def clean_rating(rating):
    """
    Convert rating representations (numbers, words 'Three', strings '4.5 out of 5') to float.
    """
    if pd.isna(rating) or rating is None:
        return np.nan

    if isinstance(rating, (int, float)):
        return float(rating)

    rating_str = str(rating).strip().lower()

    # Check word rating mapping
    if rating_str in RATING_MAP:
        return RATING_MAP[rating_str]

    # Extract numerical float pattern (e.g. 4.5 from '4.5 out of 5')
    match = re.search(r'\d+(?:\.\d+)?', rating_str)
    if match:
        try:
            return float(match.group())
        except ValueError:
            return np.nan

    return np.nan

def clean_text(text):
    """
    Strip leading/trailing spaces and collapse multiple whitespaces.
    """
    if pd.isna(text) or text is None:
        return ""
    text_str = str(text).strip()
    return re.sub(r'\s+', ' ', text_str)

def clean_product_dataframe(df):
    """
    Comprehensive Pandas data cleaning function for product datasets.
    Handles:
    - Currency symbols & commas in prices
    - Rating formatting & word conversions
    - Extra whitespace in string fields
    - Missing value imputation
    - Deduplication
    """
    if df.empty:
        return df

    cleaned_df = df.copy()

    # 1. Clean string fields and strip extra spaces
    for col in ['title', 'category', 'description', 'url']:
        if col in cleaned_df.columns:
            cleaned_df[col] = cleaned_df[col].apply(clean_text)

    # 2. Clean Prices (currency symbols, commas)
    if 'price' in cleaned_df.columns:
        cleaned_df['price'] = cleaned_df['price'].apply(clean_price)

    # 3. Clean Ratings
    if 'rating' in cleaned_df.columns:
        cleaned_df['rating'] = cleaned_df['rating'].apply(clean_rating)

    # 4. Handle Missing Values
    if 'title' in cleaned_df.columns:
        cleaned_df['title'] = cleaned_df['title'].replace('', 'Unknown Product').fillna('Unknown Product')
    if 'category' in cleaned_df.columns:
        cleaned_df['category'] = cleaned_df['category'].replace('', 'Uncategorized').fillna('Uncategorized')
    if 'description' in cleaned_df.columns:
        cleaned_df['description'] = cleaned_df['description'].fillna('')
    if 'url' in cleaned_df.columns:
        cleaned_df['url'] = cleaned_df['url'].fillna('')
    
    if 'price' in cleaned_df.columns:
        cleaned_df['price'] = cleaned_df['price'].fillna(0.0)
    if 'rating' in cleaned_df.columns:
        cleaned_df['rating'] = cleaned_df['rating'].fillna(0.0)

    # 5. Remove Duplicate Products
    subset_cols = [col for col in ['title', 'url'] if col in cleaned_df.columns]
    if subset_cols:
        cleaned_df = cleaned_df.drop_duplicates(subset=subset_cols, keep='first').reset_index(drop=True)

    return cleaned_df

def test_data_cleaning():
    """
    Test suite for data cleaning functionality with messy raw sample data.
    """
    print("--- Running Data Cleaning Tests ---")
    raw_data = [
        {
            "title": "  A Light in the Attic  ",
            "price": "£51.77",
            "rating": "Three",
            "description": "  It is a   poetry book.  ",
            "category": "Poetry",
            "url": "http://books.toscrape.com/catalog/a-light-in-the-attic_1000/index.html"
        },
        {
            "title": "A Light in the Attic",  # Duplicate title
            "price": "£51.77",
            "rating": "3",
            "description": "It is a poetry book.",
            "category": "Poetry",
            "url": "http://books.toscrape.com/catalog/a-light-in-the-attic_1000/index.html"
        },
        {
            "title": "  Gaming Laptop Pro  ",
            "price": "$1,299.99",
            "rating": "4.8 out of 5 stars",
            "description": "High performance laptop with   16GB RAM. ",
            "category": "  Electronics  ",
            "url": "https://example.com/laptop"
        },
        {
            "title": None,  # Missing title
            "price": "€ 45,50",
            "rating": None,  # Missing rating
            "description": None,
            "category": "",
            "url": None
        }
    ]

    df_raw = pd.DataFrame(raw_data)
    print(f"Raw DataFrame rows: {len(df_raw)}")
    print(df_raw[['title', 'price', 'rating']])

    df_cleaned = clean_product_dataframe(df_raw)
    print(f"\nCleaned DataFrame rows (after deduplication): {len(df_cleaned)}")
    print(df_cleaned[['title', 'price', 'rating', 'category']])
    print("\nSample Cleaned Output Record:")
    print(df_cleaned.iloc[0].to_dict())
    print("--- Data Cleaning Test Complete ---\n")

if __name__ == "__main__":
    test_data_cleaning()

