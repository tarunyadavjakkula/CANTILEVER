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

## Roadmap

- **DAY 1**: Project Setup & Environment Configuration
- **DAY 2**: Database Setup (SQLite & `products` table)
- **DAY 3+**: Web Scraper, Data Analysis & Dashboard Web Application
