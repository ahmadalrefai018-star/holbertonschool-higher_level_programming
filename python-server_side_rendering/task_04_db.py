#!/usr/bin/python3
"""Render Flask pages and display items loaded from JSON."""

import csv
import json
import sqlite3
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)
ITEMS_FILE = Path(__file__).resolve().with_name("items.json")


@app.route("/")
def home():
    """Render the home page."""
    return render_template("index.html")


@app.route("/about")
def about():
    """Render the about page."""
    return render_template("about.html")


@app.route("/contact")
def contact():
    """Render the contact page."""
    return render_template("contact.html")


@app.route("/items")
def items():
    """Load the items and render the items page."""
    with ITEMS_FILE.open(encoding="utf-8") as file:
        data = json.load(file)

    return render_template("items.html", items=data.get("items", []))


def read_json_products():
    """Read product records from the JSON file."""
    path = ITEMS_FILE.with_name("products.json")
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def read_csv_products():
    """Read product records from the CSV file."""
    path = ITEMS_FILE.with_name("products.csv")
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


DB_FILE = Path(__file__).resolve().with_name("products.db")


def read_sql_products():
    """Read products from SQLite as dictionaries."""
    with closing(sqlite3.connect(DB_FILE.as_uri() + "?mode=ro",
                                 uri=True)) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            "SELECT id, name, category, price FROM Products ORDER BY id"
        )
        return [dict(row) for row in rows]


@app.route("/products")
def products():
    """Display products from the selected source and optional ID."""
    source = request.args.get("source")
    if source == "json":
        records = read_json_products()
    elif source == "csv":
        records = read_csv_products()
    elif source == "sql":
        try:
            records = read_sql_products()
        except sqlite3.Error as error:
            app.logger.error("Could not read products from SQLite: %s", error)
            return render_template(
                "product_display.html", error="Database error"
            )
    else:
        return render_template("product_display.html", error="Wrong source")

    product_id = request.args.get("id")
    if product_id is not None:
        records = [
            product for product in records
            if str(product["id"]) == product_id
        ]
        if not records:
            return render_template(
                "product_display.html", error="Product not found"
            )

    return render_template("product_display.html", products=records)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
