from flask import jsonify
from db import db
from models.company import Companies
from models.product import Products


def add_company(req):
    post_data = req.form if req.form else req.json
    company_name = post_data.get("company_name")

    if not company_name:
        return jsonify({"message": "name is required for creating company."}), 400

    new_company = Companies(company_name)

    db.session.add(new_company)
    db.session.commit()

    return jsonify({"message": f'company {company_name} has been added to the db'}), 201


def get_all_companies(req):
    comps = db.session.query(Companies).all()

    company_list = []
    for company in comps:
        company_data = {
            "company_id":company.company_id,
            "company_name":company.company_name
        }
        company_list.append(company_data)

    return jsonify({"companies": company_list}), 200


def update_company(req, company_id):
    post_data = req.form if req.form else req.json
    new_company_name = post_data.get("company_name")

    if not new_company_name:
        return jsonify({"message": "new company name is required for updating the company."}), 400

    company = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company:
        return jsonify({"message": f"no company found with company id {company_id}"}), 404

    company.company_name = new_company_name

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": f"could not update company with company id {company_id}"}), 400

    return jsonify({"message": f"company with company id {company_id} has been updated to {new_company_name}"}), 200


def get_company_by_id(req,company_id):

    company = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company:
        return jsonify({"message": f"no company found with company id {company_id}"}), 404
    

    company_data = {
        "company_id": company.company_id,
        "company_name": company.company_name
    }

    return jsonify({"company":"company found!", "results": company_data}), 200

def delete_company(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": f"no company found with company id {company_id}"}), 404
    
    try:
        db.session.query(Products).filter(Products.company_id == company_id).delete()

        db.session.delete(company_query)
        db.session.commit()

        return jsonify({"message": f"company with company id {company_id} and associated products have been deleted"})
    except:
        db.session.rollback()
        return jsonify({"message": f"unable to delete company: {company_id}"}), 400
