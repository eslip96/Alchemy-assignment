from flask import jsonify
from db import db
from models.category import Categories


def create_category(req):
    post_data = req.form if req.form else req.get_json()
    category_name = post_data.get("category_name")

    if not category_name:
        return jsonify({"message": "category name is required for creating a category."}), 400

    new_category = Categories(category_name)

    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": f'category {category_name} with id has been added to the database'}), 201


def get_all_categories(req):
    cats = db.session.query(Categories).all()

    category_list = []
    for category in cats:
        category_data = {
            'category_id': category.category_id,
            'category_name': category.category_name
        }
        category_list.append(category_data)

    return jsonify({'categories': category_list}), 200

def update_category(req, category_id):
    post_data = req.form if req.form else req.get_json()
    new_category_name = post_data.get("category_name")

    if not new_category_name:
        return jsonify({"message": "new category name is required"}), 400
        
    category = Categories.query.get(category_id)

    if not category:
        return jsonify({"message": f"no category found with id {category_id}"}), 404

    category.category_name = new_category_name

    try:
        db.session.commit()
        return jsonify({"message": f"category with id {category_id} has been updated"}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update category"}), 404

def get_category_by_id(req, category_id):
    category = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category:
        return jsonify({"message": f"no category found with category id {category_id}"}), 404

    category_data = {
        'category_id': category.category_id,
        'category_name': category.category_name
    }

    return jsonify({"message":"category found!", "results": category_data}), 200

def delete_category(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({'message': f"no category found category id {category_id}"}), 404
    
    try:
        db.session.delete(category_query)
        db.session.commit()
        return jsonify({'message': f'category id {category_id} has been deleted'}), 200
    except:
        db.session.rollback()
        return jsonify({"message":"unable to delete category"}), 400