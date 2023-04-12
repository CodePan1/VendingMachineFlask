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


def get_required_fields_for_request(request_method):
    required_fields_of_requests = {
        "POST": {"name", "price", "quantity", "vending_machine_id"},
        "PUT": {"id"},
        "DELETE": {"id"},
    }
    return required_fields_of_requests.get(request_method, set())


def get_method_to_function_map(api_functions):
    return {
        "POST": api_functions[0],
        "PUT": api_functions[1],
        "DELETE": api_functions[2],
    }


def is_valid_fields(data, required_fields):
    return bool(data) and required_fields <= data.keys()


def make_error_response(status_code):
    return make_response(jsonify({"status": "Bad Request"}), status_code)


def make_success_response(status_code):
    return make_response(jsonify({"status": "Success"}), status_code)


def list_objects(model_class):
    objects = model_class.query.all()
    return jsonify({model_class.__name__.lower(): objects})


def modify_object(data, required_fields, method_to_function_map):
    if not is_valid_fields(data, required_fields):
        return {"status": "Bad Request"}, 400

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
