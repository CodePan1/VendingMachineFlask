import pytest

from src import create_app, db
from src.api.vending_machine_api import create_vending_machine, delete_vending_machine, update_vending_machine
from src.models.vending_machine import VendingMachine


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
def test_vm():
    new_vm = VendingMachine(name="Test VM", location="Test Location")
    db.session.add(new_vm)
    db.session.commit()
    return new_vm


def test_create_vending_machine(test_app):
    data = {
        "name": "Test Vending Machine1",
        "location": "Test Location",
    }
    status, status_code = create_vending_machine(data)
    assert status_code == 200
    assert status["status"] == "OK"
    assert VendingMachine.query.count() == 1
    data = {
        "name": "Test Vending Machine2",
        "location": "Test Location",
    }
    status, status_code = create_vending_machine(data)
    assert status_code == 200
    assert status["status"] == "OK"
    assert VendingMachine.query.count() == 2

    # Test missing required fields
    data = {
        "name": "Test Vending Machine2",
    }
    status, status_code = create_vending_machine(data)
    assert status_code == 400
    assert status["status"] == "Bad Request"
    assert VendingMachine.query.count() == 2


def test_update_vending_machine(test_app, test_vm):
    data = {
        "id": test_vm.id,
        "name": "Updated VM",
        "location": "Updated Location",
    }
    status, status_code = update_vending_machine(data)
    assert status_code == 200
    assert status["status"] == "OK"

    updated_vm = db.session.get(VendingMachine, test_vm.id)
    assert updated_vm.name == "Updated VM"
    assert updated_vm.location == "Updated VM"

    # Test invalid vending machine ID
    data["id"] = -1
    status, status_code = update_vending_machine(data)
    assert status_code == 400
    assert status["status"] == "Bad Request"


def test_delete_vending_machine(test_app, test_vm):
    data = {"id": test_vm.id}
    status, status_code = delete_vending_machine(data)
    assert status_code == 200
    assert status["status"] == "OK"
    assert VendingMachine.query.count() == 0

    # Test invalid vending machine ID
    data["id"] = -1
    status, status_code = delete_vending_machine(data)
    assert status_code == 400
    assert status["status"] == "Bad Request"
