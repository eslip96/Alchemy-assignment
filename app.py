from flask import Flask, jsonify, request
import psycopg2

import os
from db import *
from models.category import Categories
from models.company import Companies
from models.product import Products
from models.product_category_xref import products_categories_association_table

from routes.companies_routes import companies
from routes.categories_routes import categories
from routes.products_routes import products


app = Flask(__name__)

app_host = os.getenv('APP_HOST')
app_port = os.getenv('APP_PORT')

app.register_blueprint(companies)
app.register_blueprint(categories)
app.register_blueprint(products)

database_scheme = os.environ.get("DATABASE_SCHEME")
database_user = os.environ.get("DATABASE_USER")
database_address = os.environ.get("DATABASE_ADDRESS")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://127.0.0.1:5432/{database_name}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app, db)


def create_tables():
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created succesfully")


if __name__ == '__main__':
    create_tables()
    app.run(host=app_host, port=app_port, debug=True)
