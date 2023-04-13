from decimal import Decimal

import pytest

from src import create_app, db
from src.api.product_api import create_product, delete_product, update_product
from src.api.vending_machine_api import create_vending_machine, delete_vending_machine, update_vending_machine
from src.models import VendingMachine
from src.models.product import Product


@pytest.fixture
def test_app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def test_vm(test_app):
    new_vm_data = {
        "name": "Test Vending Machine",
        "location": "Test Location",
    }
    status, status_code = create_vending_machine(new_vm_data)
    assert status_code == 200
    assert status["status"] == "OK"
    assert VendingMachine.query.count() == 1
    new_vm = VendingMachine.query.first()
    yield new_vm
    delete_vending_machine({"id": new_vm.id})


def test_create_product(test_app, test_vm):
    data = {
        "name": "Test Product",
        "price": Decimal("1.99"),
        "quantity": 10,
        "vending_machine_id": test_vm.id,
    }
    status, status_code = create_product(data)
    assert status_code == 200
    assert status["status"] == "OK"
    assert Product.query.count() == 1
    new_product = Product.query.first()
    assert new_product.name == "Test Product"
    assert new_product.price == Decimal("1.99")
    assert new_product.quantity == 10
    assert new_product.vending_machine_id == test_vm.id


def test_update_product(test_app, test_vm):
    # Test updating the product name only
    new_product_data = {
        "name": "Test Product",
        "price": 1.99,
        "quantity": 10,
        "vending_machine_id": test_vm.id,
    }
    status, status_code = create_product(new_product_data)
    assert status_code == 200
    assert status["status"] == "OK"
    assert Product.query.count() == 1
    new_product = Product.query.first()

    updated_product_data = {
        "id": new_product.id,
        "name": "Updated Product Name",
        "price": Decimal("1.99"),
        "quantity": 10,
        "vending_machine_id": test_vm.id,
    }
    status, status_code = update_product(updated_product_data)
    assert status_code == 200
    assert status["status"] == "OK"

    updated_product = db.session.get(Product, new_product.id)
    assert updated_product.name == "Updated Product Name"
    assert updated_product.price == Decimal("1.99")
    assert updated_product.quantity == 10

    # Test updating the product price only
    updated_product_data = {
        "id": new_product.id,
        "name": "Updated Product Name",
        "price": Decimal("2.99"),
        "quantity": 10,
        "vending_machine_id": test_vm.id,
    }
    status, status_code = update_product(updated_product_data)
    assert status_code == 200
    assert status["status"] == "OK"

    updated_product = db.session.get(Product, new_product.id)
    assert updated_product.name == "Updated Product Name"
    assert updated_product.price == Decimal("2.99")
    assert updated_product.quantity == 10

    # Test updating the product quantity only
    updated_product_data = {
        "id": new_product.id,
        "name": "Updated Product Name",
        "price": Decimal("2.99"),
        "quantity": 20,
        "vending_machine_id": test_vm.id,
    }
    status, status_code = update_product(updated_product_data)
    assert status_code == 200
    assert status["status"] == "OK"

    updated_product = db.session.get(Product, new_product.id)
    assert updated_product.name == "Updated Product Name"
    assert updated_product.price == Decimal("2.99")
    assert updated_product.quantity == 20

    # Test updating the vending machine ID only
    new_vm = VendingMachine(location="Test Location 2")
    db.session.add(new_vm)
    db.session.commit()

    updated_product_data = {
        "id": new_product.id,
        "name": "Updated Product Name",
        "price": Decimal("2.99"),
        "quantity": 20,
        "vending_machine_id": new_vm.id,
    }
    status, status_code = update_product(updated_product_data)
    assert status_code == 200
    assert status["status"] == "OK"

    updated_product = db.session.get(Product, new_product.id)
    assert updated_product.name == "Updated Product Name"
    assert updated_product.price == Decimal("2.99")
    assert updated_product.quantity == 20
    assert updated_product.vending_machine_id == new_vm.id

    # Test invalid product ID
    updated_product_data["id"] = -1
    status, status_code = update_product(updated_product_data)
    assert status_code == 400
    assert status["status"] == "Bad Request"


def test_delete_product(test_app, test_vm):
    new_product_data = {
        "name": "Test Product",
        "price": 1.99,
        "quantity": 10,
        "vending_machine_id": test_vm.id,
    }
    status, status_code = create_product(new_product_data)
    assert status_code == 200
    assert status["status"] == "OK"
    assert Product.query.count() == 1
    new_product = Product.query.first()

    data = {"id": new_product.id}
    status, status_code = delete_product(data)
    assert status_code == 200
    assert status["status"] == "OK"
    assert Product.query.count() == 0

    # Test invalid product ID
    data["id"] = -1
    status, status_code = delete_product(data)
    assert status_code == 400
    assert status["status"] == "Bad Request"
