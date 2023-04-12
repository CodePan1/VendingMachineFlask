from ..models import VendingMachine, db

BAD_REQUEST_RESPONSE = {"status": "Bad Request"}, 400
OK_RESPONSE = {"status": "OK"}, 200


def get_vending_machine_by_id(id):
    return VendingMachine.query.filter_by(id=id).first()


def create_vending_machine(data):
    name, location = data.get("name"), data.get("location")
    if name is None or location is None:
        return BAD_REQUEST_RESPONSE
    new_vending_machine = VendingMachine(name=name, location=location)
    db.session.add(new_vending_machine)
    db.session.commit()
    return OK_RESPONSE


def update_vending_machine(data):
    id, name, location = data.get("id"), data.get("name"), data.get("location")
    vending_machine = get_vending_machine_by_id(id)
    if vending_machine is None:
        return BAD_REQUEST_RESPONSE
    if name is not None:
        vending_machine.name = name
    if location is not None:
        vending_machine.location = name
    db.session.commit()
    return OK_RESPONSE


def delete_vending_machine(data):
    id = data.get("id")
    vending_machine = get_vending_machine_by_id(id)
    if vending_machine is None:
        return BAD_REQUEST_RESPONSE
    db.session.delete(vending_machine)
    db.session.commit()
    return OK_RESPONSE
