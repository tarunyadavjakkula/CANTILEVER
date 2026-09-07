# CantiLever Internship Task 1: E-Commerce Web Scraper & Analytics Dashboard

An end-to-end Python e-commerce web scraping, data cleaning, analysis, visualization, and Flask web application pipeline.

---

## 1. Project Overview

This project builds a complete, runnable e-commerce data solution using Python. It scrapes real product data from the permitted public demo e-commerce site **Books to Scrape** (`http://books.toscrape.com/`), cleans and validates the raw fields, persists the dataset to both CSV and SQLite database storage, performs exploratory data analysis, generates custom visual analytics charts using Matplotlib, and presents an interactive web application built with Flask for exploring, searching, filtering, and sorting product listings.

---

## 2. Key Objectives

- **Automated Scraping**: Extract product title, price, rating, description, category, and canonical URL across multi-page catalog listings.
- **Data Hygiene**: Clean currency symbols, format ratings to float numbers, handle missing values, and prevent duplicates.
- **Dual Persistence**: Store processed data automatically in `data/products.csv` and SQLite `data/products.db`.
- **Exploratory Analysis**: Generate summary statistics and output 4 Matplotlib chart visualizations to `visualizations/`.
- **Web Application**: Provide a Flask web server with real-time search, multi-field filtering, sorting, detailed product views, and embedded visual analytics.

---

## 3. Technologies Used

- **Language**: Python 3.10+
- **Web Scraping**: `requests`, `BeautifulSoup4`
- **Data Processing & Storage**: `Pandas`, `SQLite3`
- **Visual Analytics**: `Matplotlib`
- **Web Framework**: `Flask` (Jinja2, HTML5, Vanilla CSS)

---

## 4. Project Structure

```text
cantiliver-task1/
│
├── scraper.py          # Web scraper module with multi-page pagination & auto-pipeline execution
├── database.py         # SQLite database schema, connections, and query operations
├── analysis.py         # Data cleaning, statistical summary analysis, and chart generation
├── app.py              # Flask web application server with routes & search/filter/sort logic
├── requirements.txt    # Project Python dependencies
├── README.md           # Project workflow and documentation
│
├── data/
│   ├── products.csv    # Automatically generated cleaned product dataset (CSV)
│   └── products.db     # SQLite database storing products table
│
├── visualizations/     # Automatically generated visual charts
│   ├── price_distribution.png
│   ├── rating_distribution.png
│   ├── price_vs_rating.png
│   └── category_prices.png
│
├── templates/
│   ├── index.html      # Product explorer catalog & analytics dashboard view
│   ├── product.html    # Individual product details page view
│   └── 404.html        # Custom 404 error page view
│
└── static/
    └── style.css       # Clean, modern custom stylesheet
```

---

## 5. End-to-End Project Workflow

```text
E-commerce Website (Books to Scrape)
        ↓
    Web Scraper (scraper.py)
        ↓
Data Cleaning & Validation (analysis.py)
        ↓
   CSV + SQLite Database (data/products.csv & data/products.db)
        ↓
   Data Analysis (analysis.py summary statistics)
        ↓
 Visualizations (Matplotlib charts in visualizations/)
        ↓
Flask Web Interface (app.py)
        ↓
 Search / Filter / Sort (title/category search, price range, ratings, sorting)
        ↓
 Product Details (/product/<id>)
        ↓
 Analytics Dashboard (Integrated metrics & chart gallery)
```

### Workflow Steps Explained:
1. **E-Commerce Website**: HTTP requests are sent to *Books to Scrape* respecting ethical crawling guidelines.
2. **Web Scraper**: Extracts product links across pagination pages and fetches detail attributes (title, price, rating, category, description, URL).
3. **Data Cleaning**: Strips currency symbols (`£`), converts word ratings (`One`..`Five`) to numerical floats (`1.0`..`5.0`), imputes missing fields, and eliminates duplicates.
4. **CSV & SQLite**: Cleaned records are written to `data/products.csv` using Pandas and inserted into `data/products.db` using SQLite with URL uniqueness constraints.
5. **Data Analysis**: Computes metrics including total products count, average price, min/max price, average rating, cheapest/most expensive items, and category breakdowns.
6. **Visualizations**: Matplotlib plots 4 charts (`price_distribution.png`, `rating_distribution.png`, `price_vs_rating.png`, `category_prices.png`).
7. **Flask Application**: Reads products from SQLite and serves an interactive product explorer UI.
8. **Search / Filter / Sort**: Supports real-time text query, category selection, price ranges, star rating filtering, and 4 sorting modes.
9. **Product Details**: Displays deep-dive information for any selected product.
10. **Analytics Dashboard**: Displays key metric cards and embeds visual charts directly in the web UI.

---

## 6. Main Features

- **Multi-Page Web Scraping**: Automatically traverses catalog pagination pages to extract products across categories.
- **Robust Data Cleaning**: Automatic type conversions, text normalization, missing value handling, and duplicate prevention.
- **Combined Search & Multi-Filter**: Search by title, description, or category while applying price bounds and min rating filters simultaneously.
- **Dynamic Sorting**: Sort product items by Price (Low to High, High to Low) or Rating (High to Low, Low to High).
- **Product Details Page**: Full information page for each product with direct links to original source web pages.
- **Visual Analytics Section**: 4 high-DPI visual graphs embedded directly in the web explorer interface.
- **Graceful Error Handling**: Custom 404 error page for non-existent product IDs and friendly empty state views for un-matched queries.

---

## 7. Installation & Setup

1. **Clone or Navigate to Project Directory**:
   ```bash
   cd cantiliver-task1
   ```

2. **Activate Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 8. How to Run the Project Components

### Step 1: Run the Web Scraper Pipeline
Run `scraper.py` to scrape real products, clean data, export to CSV/SQLite, and generate initial analytics & charts:
```bash
python scraper.py
```
*(Alternatively using venv python directly: `./venv/bin/python scraper.py`)*

### Step 2: Run Data Analysis & Visualization Standalone
To re-run statistical analysis and update visual chart images at any time:
```bash
python analysis.py
```

### Step 3: Launch the Flask Web Application
To start the web dashboard server:
```bash
python app.py
```
Open your web browser and navigate to: **`http://127.0.0.1:5000/`**

---

## 9. Visual Analytics Screenshots & Gallery

The web interface integrates four generated charts under the **Visual Analytics Dashboard** section:
- **Price Distribution**: Histogram showing product pricing ranges.
- **Rating Distribution**: Bar chart displaying frequency of star ratings (1 to 5 stars).
- **Price vs. Rating**: Scatter plot illustrating price correlation with product rating.
- **Category Prices**: Horizontal bar chart comparing average product prices across top categories.

---

## 10. Limitations

- **Demo Source Scope**: Target data source is restricted to public demo catalog pages on *Books to Scrape*.
- **Static Refresh**: Scraper must be run manually or via scheduled task to ingest newer listings into SQLite.

---

## 11. Future Improvements

- Add asynchronous HTTP crawling (e.g. using `aiohttp` or `httpx`) for faster multi-page scraping.
- Implement pagination controls on the Flask product explorer UI for large datasets (1000+ items).
- Export filtered results directly from Flask UI to CSV/Excel format.
