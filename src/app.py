"""
This module contains the Flask routes for managing machines and stock items.

The routes include functions for adding, editing, and deleting
machines and stock items.
"""

from flask import Flask, Response, jsonify, request

from src.db import db
from src.models.machine import Machine
from src.models.stock import Stock

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)


@app.route("/add/machine", methods=["POST"])
def add_machine() -> Response:
    """Add a new machine to the database.

    Returns:
        Response: A JSON response containing the request body.
    """
    content_type = request.headers.get("Content-Type")

    if content_type == "application/json":
        request_json = request.json
        new_machine = Machine(
            name=request_json["name"], location=request_json["location"]
        )
        db.session.add(new_machine)
        db.session.commit()
        return jsonify(request_json)


@app.route("/edit/machine/<int:id>", methods=["PUT"])
def edit_machine(id: int) -> Response:
    """Update an existing machine in the database.

    Args:
        id (int): The ID of the machine to update.

    Returns:
        Response: A JSON response containing a message
        indicating whether the machine was updated successfully or not.
    """
    content_type = request.headers.get("Content-Type")

    if content_type == "application/json":
        machine = Machine.query.filter_by(id=id).first()

        if machine:
            request_json = request.json
            machine.name = request_json.get("name", machine.name)
            machine.location = request_json.get("location", machine.location)
            db.session.commit()
            return jsonify({"message": "Machine updated successfully"})
        else:
            return jsonify({"message": "Machine not found"})


@app.route("/delete/machine/<int:id>", methods=["DELETE"])
def delete_machine(id: int) -> Response:
    """Delete an existing machine from the database.

    Args:
        id (int): The ID of the machine to delete.

    Returns:
        Response: A JSON response containing a message
        indicating whether the machine was deleted successfully or not.
    """
    machine = Machine.query.filter_by(id=id).first()

    if machine:
        db.session.delete(machine)
        db.session.commit()
        return jsonify({"message": "Machine deleted successfully"})
    else:
        return jsonify({"message": "Machine not found"})


@app.route("/add/stock/<int:machine_id>", methods=["POST"])
def add_stock(machine_id: int) -> Response:
    """Add new stock items to a machine in the database.

    Args:
        machine_id (int): The ID of the machine to add stock to.

    Returns:
        Response: A JSON response containing a message
        indicating whether the stock was added successfully or not.
    """
    # retrieve the Machine instance with the given machine_id
    machine = Machine.query.get(machine_id)

    if machine is None:
        return error_response(f"Machine with id {machine_id} not found")

    # create new Stock instances for the stock items provided
    stock_items = request.json
    new_stock_items = []
    for item in stock_items["items"]:
        new_stock_item = Stock(
            machine_id=machine.id,
            product_name=item["product_name"],
            quantity=item["quantity"],
        )
        new_stock_items.append(new_stock_item)

    # add the new Stock instances to the database session and commit changes
    db.session.add_all(new_stock_items)
    db.session.commit()

    return jsonify(
        {
            "status": "success",
            "message": f"Stock added successfully to machine {machine.name}.",
        }
    )


@app.route("/edit/stock/<int:stock_id>", methods=["PUT"])
def edit_stock(stock_id: int) -> Response:
    """Update the quantity of an existing stock item in the database.

    Args:
        stock_id (int): The ID of the stock item to update.

    Returns:
        Response: A JSON response containing a message
        indicating whether the stock item was updated successfully or not.
    """
    # retrieve the Stock instance with the given stock_id
    stock_item = Stock.query.get(stock_id)

    if stock_item is None:
        return error_response(f"Stock item with id {stock_id} not found")

    # update the quantity of the Stock instance
    # with the new quantity provided in the request body
    data = request.get_json()
    new_quantity = data.get("quantity")
    if new_quantity is not None:
        stock_item.quantity = new_quantity
        db.session.commit()

    return jsonify(
        {
            "status": "success",
            "message": f"Stock item with id {stock_id} updated successfully",
        }
    )


@app.route("/delete/stock/<int:stock_id>", methods=["DELETE"])
def delete_stock(stock_id: int) -> Response:
    """Delete an existing stock item from the database.

    Args:
        stock_id (int): The ID of the stock item to delete.

    Returns:
        Response: A JSON response containing a message
        indicating whether the stock item was deleted successfully or not.
    """
    # retrieve the Stock instance with the given stock_id
    stock_item = Stock.query.get(stock_id)

    if stock_item is None:
        return error_response(f"Stock item with id {stock_id} not found")

    # delete the Stock instance from the database
    db.session.delete(stock_item)
    db.session.commit()

    return jsonify(
        {
            "status": "success",
            "message": f"Stock item with id {stock_id} deleted successfully",
        }
    )


def error_response(message: str) -> jsonify:
    """Return a JSON response with an error message."""
    return jsonify({"status": "error", "message": message})


if __name__ == "__main__":
    app.run(debug=True)
