# VendingMachineFlask
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=CodePan1_VendingMachineFlask&metric=coverage)](https://sonarcloud.io/summary/new_code?id=CodePan1_VendingMachineFlask)<br />
This is a API for managing vending machines and their products. It provides CRUD operations for vending machines, products, and stock timelines.

## Requirement
```
poetry install
poetry run pre-commit install
```

## Features

- Manage vending machines (create, read, update, delete)
- Manage products (create, read, update, delete)
- View product stock timelines
- View vending machine stock timelines

## API Endpoints

### VendingMachine
POST /vending_machine - Create a new vending machine<br />
Request body: {"name": "<vending_machine_name>", "location": "<vending_machine_location>"}<br />
<br />
PUT /vending_machine - Update an existing vending machine<br />
Request body: {"id": <vending_machine_id>, "name": "<new_vending_machine_name>", "location": "<new_vending_machine_location>"}<br />
<br />
DELETE /vending_machine - Delete a vending machine<br />
Request body: {"id": <vending_machine_id>}<br />

### Product
POST /product - Create a new product<br />
Request body: {"name": "<product_name>", "price": <product_price>, "quantity": <product_quantity>, "vending_machine_id": <vending_machine_id>}<br />
<br />
PUT /product - Update an existing product<br />
Request body: {"id": <product_id>, "name": "<new_product_name>", "price": <new_product_price>, "quantity": <new_product_quantity>, "vending_machine_id": <new_vending_machine_id>}<br />
<br />
DELETE /product - Delete a product<br />
Request body: {"id": <product_id>}<br />

### Stock Timeline
GET /stock_timeline/product/<int:product_id> - Get the stock timeline for a product<br />
GET /stock_timeline/vending_machine/<int:vending_machine_id> - Get the stock timeline for a vending machine<br />

## Running Tests
```
poetry run pytest
```
