import json
import unittest

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src import db, routes  # Replace 'your_app_name' with your actual application name

app = Flask(__name__)
app.config["TESTING"] = True
app.register_blueprint(routes.routes)
test_client = app.test_client()

# Configure a test database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Create test database tables and session
test_db_engine = create_engine("sqlite:///test.db")
test_db_session = scoped_session(sessionmaker(bind=test_db_engine))


class TestRoutes(unittest.TestCase):
    def setUp(self):
        app.app_context().push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_and_delete_product(self):
        # Test product creation
        data = {
            "name": "Test Product",
            "price": 1.99,
            "quantity": 10,
            "vending_machine_id": 1,
        }
        response = test_client.post("/product", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # Test product deletion
        data = {"id": 1}
        response = test_client.delete("/product", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_create_and_delete_vending_machine(self):
        # Test vending machine creation
        data = {"name": "Test Vending Machine", "location": "Test Location"}
        response = test_client.post("/vending_machine", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # Test vending machine deletion
        data = {"id": 1}
        response = test_client.delete("/vending_machine", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_update_product(self):
        # Create a product to update
        data = {
            "name": "Test Product",
            "price": 1.99,
            "quantity": 10,
            "vending_machine_id": 1,
        }
        test_client.post("/product", data=json.dumps(data), content_type="application/json")

        # Test product update
        data = {
            "id": 1,
            "name": "Updated Test Product",
            "price": 2.99,
            "quantity": 5,
            "vending_machine_id": 2,
        }
        response = test_client.put("/product", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_update_vending_machine(self):
        # Create a vending machine to update
        data = {"name": "Test Vending Machine", "location": "Test Location"}
        test_client.post("/vending_machine", data=json.dumps(data), content_type="application/json")

        # Test vending machine update
        data = {
            "id": 1,
            "name": "Updated Test Vending Machine",
            "location": "Updated Test Location",
        }
        response = test_client.put("/vending_machine", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
