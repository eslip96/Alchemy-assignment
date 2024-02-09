from flask import jsonify
from db import db
from models.product import Products
from models.company import Companies
from models.product_category_xref import products_categories_association_table

def add_product(req):
    post_data = req.json

    product_name = post_data.get("product_name")
    description = post_data.get("description")
    price = post_data.get("price")
    active = post_data.get("active")
    company_id = post_data.get("company_id")

    if not product_name:
        return jsonify({"message": "product name required"}), 400
    
    if not price:
        return jsonify({"message": "price required"}), 400
    
    if not company_id:
        return jsonify({"message": "company_id is required"}), 400
    

    new_product = Products(
        product_name=product_name,
        description=description,
        price=price,
        active=active,
        company_id=company_id
    )
    
    try:
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": f"product {product_name} has been added"}), 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "failed to create product. try again"}), 400

def get_all_products(req):
    prods = db.session.query(Products).all()

    products_list = []
    for product in prods:
        product_data = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'description': product.description,
            'price': product.price,
            'active': product.active,
            'company_id': product.company_id,
        }
        products_list.append(product_data)

    return jsonify({'products': products_list}), 200

def get_active_products(req):
    prods = db.session.query(Products).filter(Products.active == True).all()

    products_list = []
    for product in prods:
        product_data = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'description': product.description,
            'price': product.price,
            'active': product.active,
            'company_id': product.company_id,
        }
        products_list.append(product_data)

    return jsonify({'products': products_list}), 200


def get_product_by_id(req, product_id):
    prods = db.session.query(Products).filter(Products.product_id == product_id).first()

    if prods:

        product_data = {
            'product_id': prods.product_id,
            'product_name': prods.product_name,
            'description': prods.description,
            'price': prods.price,
            'active': prods.active,
            'company_id': prods.company_id,
            'categories': prods.categories,
        }
        return jsonify({"message": product_data})    
    else:
        return jsonify({'message': 'product not found'}), 404


def update_product(req, product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()
    if not query:
        return jsonify({"message":f"no product found with id{product_id}."}), 404
 
    update_data = req.form if req.form else req.json

    query.product_name = update_data.get("product_name", query.product_name)
    query.description = update_data.get("description", query.description)
    query.price = update_data.get("price", query.price)
    query.company_id = update_data.get("company_id", query.active)
    query.active = update_data.get("active", query.active)


    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message":"unable to update record"}), 400
    
    updated_data = {
        'product_id': query.product_id,
        'product_name': query.product_name,
        'description': query.description,
        'price': query.price,
        'company_id': query.company_id,
        'active': query.active
    }

    return jsonify({'message': 'product updated', 'results': updated_data}), 200




def get_products_by_company_id(company_id):
    products = db.session.query(Products).filter(Products.company_id == company_id).all()

    if not products:
        return jsonify({"message": f"No products found for company id {company_id}"}), 404

    products_list = []
    for product in products:
        product_data = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'description': product.description,
            'price': product.price,
            'active': product.active,
            'company_id': product.company_id,
        }
        products_list.append(product_data)

    return jsonify(products_list)

def delete_product(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": f"no product found with product id {product_id}"}), 404

    try:
        db.session.query(products_categories_association_table).filter(products_categories_association_table.c.product_id == product_id).delete()
        db.session.delete(product_query)
        db.session.commit()
        return jsonify({"message":f"product with product id {product_id} has been deleted"}), 200
    except:
        db.session.rollback()
        return jsonify({"message":"unable to delete product"}),404