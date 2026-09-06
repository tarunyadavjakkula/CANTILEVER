# Task 1 - E-Commerce Web Scraper & Analytics Dashboard

An end-to-end Python e-commerce web scraping, analysis, and web dashboard project.

## Project Structure

```text
task1-ecommerce/
├── data/              # SQLite database and raw data storage
│   └── products.db
├── visualizations/    # Generated plots and visual charts
├── templates/         # HTML templates for Flask web app
├── static/            # CSS, JS, and image assets
├── scraper.py         # Web scraping module
├── database.py        # SQLite database schema and operations
├── analysis.py        # Data analysis and visualization scripts
├── app.py             # Flask web application server
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation
```

## Setup & Installation

1. **Activate Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Database**:
   ```bash
   python database.py
   ```

## Target E-Commerce Data Source Research

### Source Selection: [Books to Scrape](http://books.toscrape.com/)

**Books to Scrape** is an open e-commerce platform explicitly created for web scraping testing and education.

#### Data Source Findings:
- **Available Products**: ~1,000 book products across 50 distinct categories (e.g., *Travel, Mystery, Historical Fiction, Sequential Art, Poetry, Science*).
- **Extracted Fields**:
  - **Title**: Product headline/name (string)
  - **Price**: Original listing price in GBP `£` (float format e.g. `51.77`)
  - **Rating**: Star rating represented as word classes (`One`, `Two`, `Three`, `Four`, `Five`) converted to numeric float (`1.0` - `5.0`)
  - **Description**: Paragraph summary describing the item text
  - **Category**: Parent genre/category name (string)
  - **URL**: Direct canonical link to the individual product page
- **HTML Structure**:
  - Grid Listing Container: `<article class="product_pod">`
  - Title Anchor Tag: `<h3><a href="...">Title</a></h3>`
  - Price Tag: `<p class="price_color">£XX.XX</p>`
  - Star Rating Element: `<p class="star-rating <RatingWord>">`
  - Product Detail Page: `<div class="product_main">` with `<div id="product_description">`
- **Pagination & Structure**: Category side navigation (`ul.nav-list`) with multi-page pagination controls (`li.current`, `li.next`).
- **Ethical & Compliance Standards**: Automated HTTP requests are permitted under terms of use. No CAPTCHA, authentication bypass, header spoofing, or anti-bot evasions are required.

## Roadmap

- **DAY 1**: Project Setup & Environment Configuration
- **DAY 2**: Database Setup (SQLite & `products` table)
- **DAY 3**: Database CRUD Operations (`database.py`)
- **DAY 4**: Data Cleaning & Processing Pipeline (`analysis.py`)
- **DAY 5**: E-Commerce Data Source Selection & Research (`README.md`)
- **DAY 6**: Basic Web Scraper (`scraper.py`)
- **DAY 7**: Full Product Fields Extraction (`scraper.py`)

