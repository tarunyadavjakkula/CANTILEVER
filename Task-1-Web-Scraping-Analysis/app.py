"""
Flask Web Application Server for E-Commerce Dashboard.
"""
import os
from flask import Flask, render_template, request, send_from_directory, abort
import database

app = Flask(__name__)

VISUALIZATIONS_DIR = os.path.join(app.root_path, 'visualizations')

@app.route("/")
def home():
    """
    Main product listing explorer and analytics dashboard route.
    Supports query parameters:
    - q: search keyword (title, description, category)
    - category: selected category filter
    - min_price: minimum price filter
    - max_price: maximum price filter
    - min_rating: minimum star rating filter
    - sort_by: sorting order (price_asc, price_desc, rating_desc, rating_asc)
    """
    # Extract query parameters
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    min_price = request.args.get('min_price', '').strip()
    max_price = request.args.get('max_price', '').strip()
    min_rating = request.args.get('min_rating', '').strip()
    sort_by = request.args.get('sort_by', '').strip()

    # Query filtered products from database
    products = database.get_filtered_products(
        query=query,
        category=category,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        sort_by=sort_by
    )

    # Get distinct categories for dropdown filter
    categories = database.get_categories()

    # Get analytics summary stats
    analytics = database.get_analytics_summary()

    # Check available visualization charts
    charts = {
        'price_distribution': 'visualizations/price_distribution.png' if os.path.exists(os.path.join(VISUALIZATIONS_DIR, 'price_distribution.png')) else None,
        'rating_distribution': 'visualizations/rating_distribution.png' if os.path.exists(os.path.join(VISUALIZATIONS_DIR, 'rating_distribution.png')) else None,
        'price_vs_rating': 'visualizations/price_vs_rating.png' if os.path.exists(os.path.join(VISUALIZATIONS_DIR, 'price_vs_rating.png')) else None,
        'category_prices': 'visualizations/category_prices.png' if os.path.exists(os.path.join(VISUALIZATIONS_DIR, 'category_prices.png')) else None,
    }

    return render_template(
        "index.html",
        products=products,
        categories=categories,
        analytics=analytics,
        charts=charts,
        search_query=query,
        selected_category=category,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        sort_by=sort_by,
        total_results=len(products)
    )

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    """
    Individual product detail page route.
    """
    product = database.get_product_by_id(product_id)
    if not product:
        return render_template("404.html", message=f"Product with ID #{product_id} was not found."), 404
    return render_template("product.html", product=product)

@app.route("/visualizations/<path:filename>")
def serve_visualization(filename):
    """
    Serve generated chart image files directly from visualizations directory.
    """
    return send_from_directory(VISUALIZATIONS_DIR, filename)

@app.errorhandler(404)
def page_not_found(e):
    """
    Global 404 error handler.
    """
    return render_template("404.html", message="The page you are looking for does not exist."), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
