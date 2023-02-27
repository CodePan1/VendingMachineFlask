from flask import Flask, jsonify, request
from db import db
from models.machine import Machine
from models.stock import Stock




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)




@app.route('/add/machine/', methods=['POST'])
def add_machine():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        request_json = request.json
        new_machine = Machine(name=request_json["name"], location=request_json["location"])
        db.session.add(new_machine)
        db.session.commit()
        return jsonify(request_json)


@app.route('/edit/machine/<int:id>/', methods=['PUT'])
def edit_machine(id):
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        machine = Machine.query.filter_by(id=id).first()
        if machine:
            request_json = request.json
            machine.name = request_json.get('name', machine.name)
            machine.location = request_json.get('location', machine.location)
            db.session.commit()
            return jsonify({"message": "Machine updated successfully"})
        else:
            return jsonify({"message": "Machine not found"})


@app.route('/delete/machine/<int:id>/', methods=['DELETE'])
def delete_machine(id):
    machine = Machine.query.filter_by(id=id).first()
    if machine:
        db.session.delete(machine)
        db.session.commit()
        return jsonify({"message": "Machine deleted successfully"})
    else:
        return jsonify({"message": "Machine not found"})



@app.route('/add/stock/<int:machine_id>', methods=['POST'])
def add_stock(machine_id: int):
    # retrieve the Machine instance with the given machine_id
    machine = Machine.query.get(machine_id)

    if machine is None:
        return jsonify({"status": "error", "message": "Machine with id {} not found".format(machine_id)})

    # create new Stock instances for the stock items provided
    stock_items = request.json
    new_stock_items = []
    for item in stock_items['items']:
        new_stock_item = Stock(machine_id=machine.id, product_name=item['product_name'], quantity=item['quantity'])
        new_stock_items.append(new_stock_item)

    # add the new Stock instances to the database session and commit changes
    db.session.add_all(new_stock_items)
    db.session.commit()

    return jsonify({"status": "success", "message": "Stock added successfully to machine {}.".format(machine.name)})



@app.route('/edit/stock/<int:stock_id>', methods=['PUT'])
def edit_stock(stock_id: int):
    # retrieve the Stock instance with the given stock_id
    stock_item = Stock.query.get(stock_id)

    if stock_item is None:
        return jsonify({"status": "error", "message": "Stock item with id {} not found".format(stock_id)})

    # update the quantity of the Stock instance with the new quantity provided in the request body
    data = request.get_json()
    new_quantity = data.get('quantity')
    if new_quantity is not None:
        stock_item.quantity = new_quantity
        db.session.commit()

    return jsonify({"status": "success", "message": "Stock item with id {} updated successfully".format(stock_id)})


@app.route('/delete/stock/<int:stock_id>', methods=['DELETE'])
def delete_stock(stock_id: int):
    # retrieve the Stock instance with the given stock_id
    stock_item = Stock.query.get(stock_id)

    if stock_item is None:
        return jsonify({"status": "error", "message": "Stock item with id {} not found".format(stock_id)})

    # delete the Stock instance from the database
    db.session.delete(stock_item)
    db.session.commit()

    return jsonify({"status": "success", "message": "Stock item with id {} deleted successfully".format(stock_id)})



if __name__ == '__main__':
    app.run(debug=True)
