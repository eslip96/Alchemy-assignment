from flask import Blueprint, request, jsonify

from controllers import products_controller


products = Blueprint('products', __name__)


@products.route('/product', methods=['POST'])
def add_product():
    return products_controller.add_product(request)


@products.route('/products', methods=['GET'])
def get_all_products():
    return products_controller.get_all_products(request)


@products.route('/product/active', methods=['GET'])
def get_active_products():
    return products_controller.get_active_products(request)


@products.route('/product/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    return products_controller.get_product_by_id(request, product_id)


@products.route('/product/<product_id>', methods=['PUT'])
def update_product(product_id):
    return products_controller.update_product(request, product_id)


@products.route('/products/company/<company_id>', methods=['GET'])
def get_products_by_company_id(company_id):
    return products_controller.get_products_by_company_id(company_id)


@products.route('/product/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    return products_controller.delete_product(product_id)
