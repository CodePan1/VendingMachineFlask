from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request
from flask.helpers import make_response

from .api.product_api import create_product, delete_product, update_product
from .api.vending_machine_api import (
    create_vending_machine,
    delete_vending_machine,
    update_vending_machine,
)
from .models import Product, VendingMachine

routes = Blueprint("routes", __name__)


# Product routes
@routes.route("/product", methods=["POST"])
def create_product_route():
    data = request.get_json()
    return create_product(data)


@routes.route("/product", methods=["PUT"])
def update_product_route():
    data = request.get_json()
    return update_product(data)


@routes.route("/product", methods=["DELETE"])
def delete_product_route():
    data = request.get_json()
    return delete_product(data)


# Vending machine routes
@routes.route("/vending_machine", methods=["POST"])
def create_vending_machine_route():
    data = request.get_json()
    return create_vending_machine(data)


@routes.route("/vending_machine", methods=["PUT"])
def update_vending_machine_route():
    data = request.get_json()
    return update_vending_machine(data)


@routes.route("/vending_machine", methods=["DELETE"])
def delete_vending_machine_route():
    data = request.get_json()
    return delete_vending_machine(data)

    api_function = method_to_function_map.get(request.method)
    if api_function is None:
        return {"status": "Bad Request"}, 400

    status_code = 200
    try:
        api_function(data)
    except Exception:
        status_code = 500
        return {"status": "Internal Server Error"}, status_code

    return {"status": "Success"}, status_code


# Vending machine
@routes.route("/vending_machine")
def list_vending_machines():
    return list_objects(VendingMachine)


@routes.route("/vending_machine", methods=["POST", "PUT", "DELETE"])
def modify_vending_machine():
    required_fields = get_required_fields_for_request(request.method)
    method_to_function_map = get_method_to_function_map(
        (create_vending_machine, update_vending_machine, delete_vending_machine)
    )
    return modify_object(request.get_json(), required_fields, method_to_function_map)


# Product
@routes.route("/product")
def list_products():
    return list_objects(Product)


@routes.route("/product", methods=["POST", "PUT", "DELETE"])
def modify_product():
    required_fields = get_required_fields_for_request(request.method)
    method_to_function_map = get_method_to_function_map(
        (create_product, update_product, delete_product)
    )
    return modify_object(request.get_json(), required_fields, method_to_function_map)
