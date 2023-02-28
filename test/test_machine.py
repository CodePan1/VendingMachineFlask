"""This module contains tests for the `Machine` class."""

import json
from typing import Callable

from src.app import Machine, db


def test_create_machine(client: Callable) -> None:
    """Test creating a new vending machine."""
    data = {"name": "test_machine_01", "location": "test_location_01"}
    response = client.post(
        "/add/machine", data=json.dumps(data), content_type="application/json"
    )

    assert response.status_code == 200

    machine = Machine.query.filter_by(name=data["name"]).first()
    assert machine is not None
    assert machine.name == data["name"]
    assert machine.location == data["location"]


def test_edit_machine(client: Callable) -> None:
    """Test editing an existing vending machine."""
    machine = Machine(name="test_machine_02", location="test_location_02")
    db.session.add(machine)
    db.session.commit()

    new_data = {
        "name": "test_machine_02_edited",
        "location": "test_location_02_edited",
    }
    response = client.put(
        f"/edit/machine/{machine.id}",
        data=json.dumps(new_data),
        content_type="application/json",
    )

    assert response.status_code == 200

    updated_machine = Machine.query.filter_by(id=machine.id).first()
    assert updated_machine is not None
    assert updated_machine.name == new_data["name"]
    assert updated_machine.location == new_data["location"]


def test_delete_machine(client: Callable) -> None:
    """Test deleting an existing vending machine."""
    machine = Machine(name="test_machine_03", location="test_location_03")
    db.session.add(machine)
    db.session.commit()

    response = client.delete(f"/delete/machine/{machine.id}")

    assert response.status_code == 200

    deleted_machine = Machine.query.filter_by(id=machine.id).first()
    assert deleted_machine is None
