import json
from app import app, db, Stock, Machine


def test_add_stock_to_existing_machine(client):
    # create a new Machine instance
    machine = Machine(name='Vending Machine 1', location='123 Main St.')
    db.session.add(machine)
    db.session.commit()

    # send a POST request to add stock to the machine
    stock_items = {
        "items": [
            {"product_name": "Cola", "quantity": 10},
            {"product_name": "Chips", "quantity": 5},
            {"product_name": "Candy", "quantity": 12}
        ]
    }
    response = client.post('/add/stock/1', data=json.dumps(stock_items), content_type='application/json')

    assert response.status_code == 200
    assert b'Stock added successfully' in response.data

    # check that the stock items were added to the database
    stock_items = Stock.query.filter_by(machine_id=machine.id).all()
    assert len(stock_items) == 3
    assert stock_items[0].product_name == 'Cola'
    assert stock_items[0].quantity == 10
    assert stock_items[1].product_name == 'Chips'
    assert stock_items[1].quantity == 5
    assert stock_items[2].product_name == 'Candy'
    assert stock_items[2].quantity == 12


def test_add_stock_to_nonexistent_machine(client):
    # send a POST request to add stock to a nonexistent machine
    stock_items = {
        "items": [
            {"product_name": "Cola", "quantity": 10},
            {"product_name": "Chips", "quantity": 5},
            {"product_name": "Candy", "quantity": 12}
        ]
    }
    response = client.post('/add/stock/1', data=json.dumps(stock_items), content_type='application/json')

    assert response.status_code == 200
    assert b'Machine with id 1 not found' in response.data

    # check that no stock items were added to the database
    stock_items = Stock.query.all()
    assert len(stock_items) == 0


def test_edit_stock(client):
    # create a new Stock instance
    stock_item = Stock(machine_id=1, product_name='Cola', quantity=10)
    db.session.add(stock_item)
    db.session.commit()

    # send a PUT request to update the quantity of the stock item
    new_quantity = 5
    response = client.put(f'/edit/stock/{stock_item.id}', data=json.dumps({'quantity': new_quantity}),
                          content_type='application/json')

    assert response.status_code == 200
    assert b'Stock item with id 1 updated successfully' in response.data

    # check that the quantity of the stock item was updated in the database
    stock_item = Stock.query.get(1)
    assert stock_item.quantity == new_quantity


def test_edit_nonexistent_stock(client):
    # send a PUT request to update a nonexistent stock item
    new_quantity = 5
    response = client.put('/edit/stock/1', data=json.dumps({'quantity': new_quantity}), content_type='application/json')

    assert response.status_code == 200
    assert b'Stock item with id 1 not found' in response.data

    # check that no stock items were updated in the database
    stock_items = Stock.query.all()
    assert len(stock_items) == 0


def test_delete_existing_stock(client):
    # create a new Stock instance
    stock_item = Stock(machine_id=1, product_name='Cola', quantity=10)
    db.session.add(stock_item)
    db.session.commit()

    # send a DELETE request to delete the stock item
    response = client.delete('/delete/stock/1')

    assert response.status_code == 200
    assert b'Stock item with id 1 deleted successfully' in response.data

    # check that the stock item was deleted from the database
    stock_items = Stock.query.all()
    assert len(stock_items) == 0


def test_delete_nonexistent_stock(client):
    # send a DELETE request to delete a nonexistent stock item
    response = client.delete('/delete/stock/1')

    assert response.status_code == 200
    assert b'Stock item with id 1 not found' in response.data

    # check that no stock items were deleted from the database
    stock_items = Stock.query.all()
    assert len(stock_items) == 0
