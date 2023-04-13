# VendingMachineFlask
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=CodePan1_VendingMachineFlask&metric=coverage)](https://sonarcloud.io/summary/new_code?id=CodePan1_VendingMachineFlask)
This is a API for managing vending machines and their products. It provides CRUD operations for vending machines, products, and stock timelines.

## Features

- Manage vending machines (create, read, update, delete)
- Manage products (create, read, update, delete)
- View product stock timelines
- View vending machine stock timelines

## API Endpoints

### VendingMachine
POST /vending_machine - Create a new vending machine\n
Request body: {"name": "<vending_machine_name>", "location": "<vending_machine_location>"}
