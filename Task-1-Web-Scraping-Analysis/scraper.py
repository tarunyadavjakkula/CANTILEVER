"""
Web scraper module for e-commerce product data extraction.
Target Site: Books to Scrape (http://books.toscrape.com/)
"""
import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import pandas as pd

import database
import analysis

BASE_URL = "http://books.toscrape.com/"
CSV_PATH = "data/products.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

def fetch_page(url):
    """
    Fetch web page content using requests with header & timeout support.
    Returns BeautifulSoup object or None on network error.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"[Scraper Error] Failed to fetch URL {url}: {e}")
        return None

def extract_rating(product_div):
    """
    Extract rating string (e.g. 'One', 'Two', 'Three', 'Four', 'Five') from star-rating class.
    """
    rating_tag = product_div.find("p", class_=lambda c: c and c.startswith("star-rating"))
    if rating_tag and "class" in rating_tag.attrs:
        classes = rating_tag["class"]
        for cls in classes:
            if cls != "star-rating":
                return cls
    return "Unrated"

def scrape_product_details(product_url):
    """
    Extract complete product information fields from individual detail page:
    - Title
    - Price
    - Rating
    - Description
    - Category
    - URL
    """
    soup = fetch_page(product_url)
    if not soup:
        return None

    product_div = soup.find("div", class_="product_main")
    if not product_div:
        return None

    # 1. Title
    title_tag = product_div.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Unknown Product"

    # 2. Price
    price_tag = product_div.find("p", class_="price_color")
    price = price_tag.get_text(strip=True) if price_tag else "N/A"

    # 3. Rating
    rating = extract_rating(product_div)

    # 4. Description
    desc_header = soup.find("div", id="product_description")
    description = ""
    if desc_header:
        desc_p = desc_header.find_next_sibling("p")
        if desc_p:
            description = desc_p.get_text(strip=True)

    # 5. Category (from breadcrumbs)
    category = "Uncategorized"
    breadcrumb = soup.find("ul", class_="breadcrumb")
    if breadcrumb:
        breadcrumbs = breadcrumb.find_all("li")
        if len(breadcrumbs) >= 3:
            category = breadcrumbs[2].get_text(strip=True)

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "description": description,
        "category": category,
        "url": product_url
    }

def get_product_urls_from_page(page_url):
    """
    Extract all product detail links from a single catalog listing page,
    along with the URL of the 'Next' pagination page if present.
    """
    soup = fetch_page(page_url)
    if not soup:
        return [], None

    product_links = []
    for article in soup.find_all("article", class_="product_pod"):
        h3 = article.find("h3")
        if h3 and h3.find("a"):
            rel_link = h3.find("a")["href"]
            full_link = urljoin(page_url, rel_link)
            product_links.append(full_link)

    # Check next page pagination link
    next_page_url = None
    next_li = soup.find("li", class_="next")
    if next_li and next_li.find("a"):
        next_rel = next_li.find("a")["href"]
        next_page_url = urljoin(page_url, next_rel)

    return product_links, next_page_url

def scrape_multiple_products(limit=50, max_pages=5):
    """
    Scrape multiple product detail pages from the catalog supporting multi-page pagination.
    """
    current_page_url = BASE_URL
    all_product_urls = []
    page_count = 0

    print(f"[Scraper] Discovering product links across catalog pages (Target: ~{limit} products)...")

    while current_page_url and len(all_product_urls) < limit and page_count < max_pages:
        page_count += 1
        print(f"  - Fetching catalog page #{page_count}: {current_page_url}")
        links, next_page = get_product_urls_from_page(current_page_url)
        all_product_urls.extend(links)
        current_page_url = next_page

    # Truncate to desired limit
    target_urls = all_product_urls[:limit]
    print(f"[Scraper] Extracted {len(target_urls)} product URLs. Starting detail extraction...")

    scraped_products = []
    for idx, url in enumerate(target_urls, 1):
        print(f"  [{idx}/{len(target_urls)}] Scraping product page: {url}")
        if data := scrape_product_details(url):
            scraped_products.append(data)

    print(f"[Scraper] Successfully extracted raw details for {len(scraped_products)} products.")
    return scraped_products

def save_to_csv(df, filepath=CSV_PATH):
    """
    Save cleaned product DataFrame to CSV file.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    expected_cols = ['id', 'title', 'price', 'rating', 'description', 'category', 'url']
    for col in expected_cols:
        if col not in df.columns:
            df[col] = ""
    df = df[expected_cols]
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"[CSV Storage] Successfully saved {len(df)} products to '{filepath}'")

def run_scraper_pipeline(limit=50, max_pages=5):
    """
    Complete Scraper Workflow:
    1. Scrape raw products from web source
    2. Clean and validate data using Pandas
    3. Save cleaned data to CSV (data/products.csv)
    4. Insert cleaned data into SQLite DB (data/products.db)
    5. Run analysis & update visualization charts
    """
    print("=" * 60)
    print("        STARTING E-COMMERCE SCRAPER PIPELINE          ")
    print("=" * 60)

    # 1. Scrape
    raw_products = scrape_multiple_products(limit=limit, max_pages=max_pages)
    if not raw_products:
        print("[Scraper Pipeline] Error: No products were scraped.")
        return

    # 2. Clean & Validate
    print("[Scraper Pipeline] Cleaning and validating scraped dataset...")
    raw_df = pd.DataFrame(raw_products)
    cleaned_df = analysis.clean_product_dataframe(raw_df)

    # 3. CSV Storage
    save_to_csv(cleaned_df, CSV_PATH)

    # 4. SQLite Storage
    print("[SQLite Storage] Initializing database and inserting products...")
    database.create_database()
    database.clear_products()
    product_dicts = cleaned_df.to_dict('records')
    database.insert_products(product_dicts)
    print(f"[SQLite Storage] Inserted/updated {len(product_dicts)} products in database.")

    # 5. Analysis & Visualizations
    print("[Analysis & Visualizations] Generating analytics report and charts...")
    analysis.perform_data_analysis(cleaned_df)
    analysis.generate_visualizations(cleaned_df)

    print("=" * 60)
    print("        SCRAPER PIPELINE COMPLETED SUCCESSFULLY       ")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    run_scraper_pipeline(limit=40, max_pages=3)
