import json
import unittest

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src import db, routes

app = Flask(__name__)
app.config["TESTING"] = True
app.register_blueprint(routes.routes)
test_client = app.test_client()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

test_db_engine = create_engine("sqlite:///test.db")
test_db_session = scoped_session(sessionmaker(bind=test_db_engine))


class TestStockTimeline(unittest.TestCase):
    def setUp(self):
        app.app_context().push()
        db.create_all()

        # Create test product and vending machine instances
        product_data = {
            "name": "Test Product",
            "price": 1.99,
            "quantity": 10,
            "vending_machine_id": 1,
        }
        test_client.post("/product", data=json.dumps(product_data), content_type="application/json")

        vm_data = {"name": "Test Vending Machine", "location": "Test Location"}
        test_client.post("/vending_machine", data=json.dumps(vm_data), content_type="application/json")

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_product_stock_timeline(self):
        response = test_client.get("/stock_timeline/product/1")
        self.assertEqual(response.status_code, 200)

    def test_get_vending_machine_stock_timeline(self):
        response = test_client.get("/stock_timeline/vending_machine/1")
        self.assertEqual(response.status_code, 200)

    def test_create_product_stock_timeline(self):
        product_data = {
            "name": "Another Test Product",
            "price": 2.99,
            "quantity": 5,
            "vending_machine_id": 1,
        }
        response = test_client.post("/product", data=json.dumps(product_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        response = test_client.get("/stock_timeline/product/2")
        self.assertEqual(response.status_code, 200)

    def test_update_product_stock_timeline(self):
        update_data = {
            "id": 1,
            "quantity": 20,
        }
        response = test_client.put("/product", data=json.dumps(update_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        response = test_client.get("/stock_timeline/product/1")
        self.assertEqual(response.status_code, 200)
        timeline_entries = response.get_json()["stock_timeline"]
        self.assertEqual(len(timeline_entries), 2)

    def test_create_vending_machine_stock_timeline(self):
        vm_data = {"name": "Another Test Vending Machine", "location": "Another Test Location"}
        response = test_client.post("/vending_machine", data=json.dumps(vm_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        response = test_client.get("/stock_timeline/vending_machine/2")
        self.assertEqual(response.status_code, 200)
