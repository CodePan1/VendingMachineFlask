from flask import Blueprint, jsonify, request

from .api.product_api import create_product, delete_product, update_product
from .api.stock_timeline_api import get_product_stock_timeline, get_vending_machine_stock_timeline
from .api.vending_machine_api import create_vending_machine, delete_vending_machine, update_vending_machine
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


# Stock timeline routes
@routes.route("/stock_timeline/product/<int:product_id>", methods=["GET"])
def get_product_stock_timeline_route(product_id):
    stock_timeline = get_product_stock_timeline(product_id)
    return jsonify({"stock_timeline": [entry.to_dict() for entry in stock_timeline]}), 200


@routes.route("/stock_timeline/vending_machine/<int:vending_machine_id>", methods=["GET"])
def get_vending_machine_stock_timeline_route(vending_machine_id):
    stock_timeline = get_vending_machine_stock_timeline(vending_machine_id)
    return jsonify({"stock_timeline": [entry.to_dict() for entry in stock_timeline]}), 200
