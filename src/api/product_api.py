from ..models import Product, VendingMachine, db

BAD_REQUEST_RESPONSE = {"status": "Bad Request"}, 400
OK_RESPONSE = {"status": "OK"}, 200


def get_product(product_id):
    return Product.query.filter_by(id=product_id).first()


def create_product(data):
    name, price, quantity, vm_id = (
        data.get("name"),
        data.get("price"),
        data.get("quantity"),
        data.get("vending_machine_id"),
    )
    product = Product(
        name=name, price=price, quantity=quantity, vending_machine_id=vm_id
    )
    db.session.add(product)
    db.session.commit()
    return OK_RESPONSE


def update_product(data):
    product_id, name, price, quantity, vm_id = (
        data.get("id"),
        data.get("name"),
        data.get("price"),
        data.get("quantity"),
        data.get("vending_machine_id"),
    )
    product = get_product(product_id)
    if product is None:
        return BAD_REQUEST_RESPONSE
    if name is not None:
        product.name = name
    if price is not None:
        product.price = price
    if quantity is not None:
        product.quantity = quantity
    if vm_id is not None:
        product.vending_machine_id = vm_id
    db.session.commit()
    return OK_RESPONSE


def delete_product(data):
    product_id = data.get("id")
    product = get_product(product_id)
    if product is None:
        return BAD_REQUEST_RESPONSE
    db.session.delete(product)
    db.session.commit()
    return OK_RESPONSE
