"""
Data analysis, processing, data cleaning, and visualization module for e-commerce products.
"""
import os
import re
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for generating image files
import matplotlib.pyplot as plt

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
    subset_cols = [col for col in ['url', 'title'] if col in cleaned_df.columns]
    if subset_cols:
        cleaned_df = cleaned_df.drop_duplicates(subset=subset_cols, keep='first').reset_index(drop=True)

    # Add numeric id column if not present
    if 'id' not in cleaned_df.columns:
        cleaned_df.insert(0, 'id', range(1, len(cleaned_df) + 1))

    return cleaned_df

def perform_data_analysis(df):
    """
    Perform exploratory data analysis and return summary report dict & text.
    """
    if df.empty:
        print("[Analysis] Warning: Empty dataset provided.")
        return {}

    total_products = len(df)
    avg_price = df['price'].mean() if 'price' in df else 0.0
    min_price = df['price'].min() if 'price' in df else 0.0
    max_price = df['price'].max() if 'price' in df else 0.0
    avg_rating = df['rating'].mean() if 'rating' in df else 0.0

    cheapest_products = df.nsmallest(3, 'price')[['title', 'price', 'category']].to_dict('records') if 'price' in df else []
    most_expensive_products = df.nlargest(3, 'price')[['title', 'price', 'category']].to_dict('records') if 'price' in df else []
    highest_rated = df.nlargest(3, 'rating')[['title', 'rating', 'price']].to_dict('records') if 'rating' in df else []

    category_counts = df['category'].value_counts().to_dict() if 'category' in df else {}
    rating_counts = df['rating'].value_counts().sort_index().to_dict() if 'rating' in df else {}

    summary = {
        "total_products": total_products,
        "avg_price": round(float(avg_price), 2),
        "min_price": round(float(min_price), 2),
        "max_price": round(float(max_price), 2),
        "avg_rating": round(float(avg_rating), 2),
        "cheapest_products": cheapest_products,
        "most_expensive_products": most_expensive_products,
        "highest_rated_products": highest_rated,
        "category_counts": category_counts,
        "rating_counts": rating_counts
    }

    print("\n" + "="*50)
    print("        E-COMMERCE DATA ANALYSIS REPORT        ")
    print("="*50)
    print(f"Total Scraped Products  : {total_products}")
    print(f"Average Product Price   : £{summary['avg_price']:.2f}")
    print(f"Minimum Product Price   : £{summary['min_price']:.2f}")
    print(f"Maximum Product Price   : £{summary['max_price']:.2f}")
    print(f"Average Product Rating  : {summary['avg_rating']:.1f} / 5.0")
    print("-" * 50)
    print("Products Count by Category:")
    for cat, count in category_counts.items():
        print(f"  - {cat:<25}: {count}")
    print("-" * 50)
    print("Rating Distribution:")
    for rating_val, count in rating_counts.items():
        print(f"  - {rating_val} Stars: {count} product(s)")
    print("-" * 50)
    print("Cheapest Products:")
    for item in cheapest_products:
        print(f"  - {item['title'][:35]:<35} | £{item['price']:.2f} | {item['category']}")
    print("-" * 50)
    print("Most Expensive Products:")
    for item in most_expensive_products:
        print(f"  - {item['title'][:35]:<35} | £{item['price']:.2f} | {item['category']}")
    print("="*50 + "\n")

    return summary

def generate_visualizations(df, output_dir="visualizations"):
    """
    Generate and save the required 4 Matplotlib visualizations.
    """
    os.makedirs(output_dir, exist_ok=True)
    if df.empty:
        print("[Visualizations] Warning: DataFrame is empty. Charts skipped.")
        return

    plt.style.use('ggplot')

    # 1. Price Distribution Chart
    plt.figure(figsize=(8, 5))
    plt.hist(df['price'], bins=15, color='#4F46E5', edgecolor='#312E81', alpha=0.8)
    plt.title('Product Price Distribution', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Price (£)', fontsize=12)
    plt.ylabel('Number of Products', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    price_dist_path = os.path.join(output_dir, 'price_distribution.png')
    plt.savefig(price_dist_path, dpi=200)
    plt.close()
    print(f"[Visualizations] Saved: {price_dist_path}")

    # 2. Rating Distribution Chart
    plt.figure(figsize=(8, 5))
    rating_series = df['rating'].value_counts().sort_index()
    bars = plt.bar([str(int(r)) if r.is_integer() else str(r) for r in rating_series.index], 
                   rating_series.values, color='#10B981', edgecolor='#047857', alpha=0.85)
    plt.title('Product Rating Distribution', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Star Rating (1 - 5)', fontsize=12)
    plt.ylabel('Number of Products', fontsize=12)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{int(height)}', ha='center', va='bottom', fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    rating_dist_path = os.path.join(output_dir, 'rating_distribution.png')
    plt.savefig(rating_dist_path, dpi=200)
    plt.close()
    print(f"[Visualizations] Saved: {rating_dist_path}")

    # 3. Price vs Rating Scatter Chart
    plt.figure(figsize=(8, 5))
    plt.scatter(df['rating'], df['price'], color='#F59E0B', edgecolors='#B45309', s=60, alpha=0.75)
    plt.title('Price vs Product Rating', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Rating (Stars)', fontsize=12)
    plt.ylabel('Price (£)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    price_vs_rating_path = os.path.join(output_dir, 'price_vs_rating.png')
    plt.savefig(price_vs_rating_path, dpi=200)
    plt.close()
    print(f"[Visualizations] Saved: {price_vs_rating_path}")

    # 4. Category Prices Chart (Average price by category)
    plt.figure(figsize=(10, 5.5))
    cat_prices = df.groupby('category')['price'].mean().sort_values(ascending=False)
    # Limit to top 10 categories for clarity if there are many
    if len(cat_prices) > 10:
        cat_prices = cat_prices.head(10)
    
    bars = plt.barh(cat_prices.index[::-1], cat_prices.values[::-1], color='#6366F1', edgecolor='#4338CA', alpha=0.85)
    plt.title('Average Price by Category (Top Categories)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Average Price (£)', fontsize=12)
    plt.ylabel('Category', fontsize=12)
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.5, bar.get_y() + bar.get_height()/2., f'£{width:.2f}', ha='left', va='center', fontsize=9)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    cat_prices_path = os.path.join(output_dir, 'category_prices.png')
    plt.savefig(cat_prices_path, dpi=200)
    plt.close()
    print(f"[Visualizations] Saved: {cat_prices_path}")

def run_analysis_pipeline():
    """
    Load data from SQLite or CSV, perform data analysis, and generate plots.
    """
    import database
    database.create_database()
    products = database.get_all_products()

    if not products:
        csv_path = "data/products.csv"
        if os.path.exists(csv_path):
            print(f"[Analysis] Loading product data from CSV: {csv_path}")
            df = pd.read_csv(csv_path)
        else:
            print("[Analysis] No data found in SQLite DB or CSV. Generating sample test data for analysis...")
            from database import test_database_operations
            test_database_operations()
            products = database.get_all_products()
            df = pd.DataFrame(products)
    else:
        print(f"[Analysis] Loaded {len(products)} products from SQLite database.")
        df = pd.DataFrame(products)

    df_cleaned = clean_product_dataframe(df)
    perform_data_analysis(df_cleaned)
    generate_visualizations(df_cleaned)

if __name__ == "__main__":
    run_analysis_pipeline()
