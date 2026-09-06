"""
Web scraper module for e-commerce product data extraction.
Target Site: Books to Scrape (http://books.toscrape.com/)
"""
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
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"[Error] Failed to fetch URL {url}: {e}")
        return None

def scrape_single_product(product_url):
    """
    Basic Scraper (Day 6): Extract initial product data from a single product page URL.
    Pipeline: URL -> requests -> HTML -> BeautifulSoup
    """
    soup = fetch_page(product_url)
    if not soup:
        return None

    # Target product elements
    product_div = soup.find("div", class_="product_main")
    if not product_div:
        return None

    # Extract title and price
    title = product_div.find("h1").get_text(strip=True) if product_div.find("h1") else "N/A"
    price = product_div.find("p", class_="price_color").get_text(strip=True) if product_div.find("p", class_="price_color") else "N/A"

    return {
        "title": title,
        "price": price,
        "url": product_url
    }

def test_basic_scraper():
    """
    Test Day 6 Basic Web Scraper on a single target product.
    """
    print("--- Running Day 6 Basic Scraper Test ---")
    target_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    product = scrape_single_product(target_url)

    if product:
        print("Successfully extracted product:")
        print(f"  Title: {product['title']}")
        print(f"  Price: {product['price']}")
        print(f"  URL:   {product['url']}")
    else:
        print("Failed to extract product.")
    print("--- Basic Scraper Test Complete ---\n")

if __name__ == "__main__":
    test_basic_scraper()

