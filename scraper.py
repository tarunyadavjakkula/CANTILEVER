"""
Web scraper module for e-commerce product data extraction.
Target Site: Books to Scrape (http://books.toscrape.com/)
"""
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_page(url):
    """
    Fetch web page content using requests and return a BeautifulSoup object.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"[Error] Failed to fetch URL {url}: {e}")
        return None

def extract_rating(product_div):
    """
    Extract rating string (e.g. 'One', 'Two', 'Three', 'Four', 'Five') from star-rating class.
    """
    rating_tag = product_div.find("p", class_=lambda c: c and c.startswith("star-rating"))
    if rating_tag and "class" in rating_tag.attrs:
        classes = rating_tag["class"]
        # Find the class that isn't 'star-rating'
        for cls in classes:
            if cls != "star-rating":
                return cls
    return "Unrated"

def scrape_product_details(product_url):
    """
    Day 7: Extract complete product information fields:
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
    title = product_div.find("h1").get_text(strip=True) if product_div.find("h1") else "N/A"

    # 2. Price
    price = product_div.find("p", class_="price_color").get_text(strip=True) if product_div.find("p", class_="price_color") else "N/A"

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
    if breadcrumbs := breadcrumb.find_all("li"):
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

def get_product_urls_from_page(page_url=BASE_URL):
    """
    Extract all product detail links from a catalog listing page.
    """
    soup = fetch_page(page_url)
    if not soup:
        return []

    product_links = []
    for article in soup.find_all("article", class_="product_pod"):
        h3 = article.find("h3")
        if h3 and h3.find("a"):
            rel_link = h3.find("a")["href"]
            # Handle relative link resolution
            if "catalogue/" not in rel_link and not rel_link.startswith("http"):
                full_link = urljoin(BASE_URL + "catalogue/", rel_link)
            else:
                full_link = urljoin(BASE_URL, rel_link)
            product_links.append(full_link)

    return product_links

def scrape_multiple_products(limit=5):
    """
    Scrape multiple product detail pages from the catalog.
    """
    product_urls = get_product_urls_from_page(BASE_URL)
    scraped_products = []

    print(f"Found {len(product_urls)} products on main catalog. Scraping first {limit}...")
    for url in product_urls[:limit]:
        print(f"Scraping product page: {url}")
        if data := scrape_product_details(url):
            scraped_products.append(data)

    return scraped_products

def test_full_scraper():
    """
    Test Day 7 Full Product Field Extraction across several products.
    """
    print("--- Running Day 7 Full Product Field Extraction Test ---")
    products = scrape_multiple_products(limit=3)

    print(f"\nSuccessfully scraped {len(products)} products with full fields:\n")
    for i, p in enumerate(products, 1):
        print(f"Product #{i}:")
        print(f"  Title:       {p['title']}")
        print(f"  Price:       {p['price']}")
        print(f"  Rating:      {p['rating']}")
        print(f"  Category:    {p['category']}")
        print(f"  Description: {p['description'][:80]}..." if p['description'] else "  Description: N/A")
        print(f"  URL:         {p['url']}\n")

    print("--- Full Product Extraction Test Complete ---\n")

if __name__ == "__main__":
    test_full_scraper()


