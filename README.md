# KitchenIntel Backend (kitchenintel-be)

KitchenIntel Backend is a Django REST Framework application designed for restaurant analytics and menu intelligence. It provides APIs to manage menu categories, menu items, orders, dashboards, and data-driven insights for restaurant operations.

## Features
- Menu and category management
- Order and order item management
- Dashboard and graph analytics (weekly/monthly)
- Data seeding for rapid development/testing
- Optimized API with custom pagination

## Technology Stack
- Python 3
- Django 5
- Django REST Framework
- PostgreSQL (or SQLite for development)
- Huey (task queue)
- Pandas, Matplotlib, Seaborn (for analytics/graphs)

## Getting Started

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd kitchenintel-be
```

### 2. Install Dependencies
It is recommended to use a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment Variables
Copy the sample environment file and configure your settings:
```bash
cp .env-sample .env
# Edit .env as needed (set DB, secret key, etc)
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

## Data Generation & Seeding
This project provides management commands to generate initial data for menu categories, menus, and orders. Run these commands in order for a complete data setup.

### 1. Seed Menu Categories
```bash
python manage.py seed_menu_categories
```
This will create parent and child menu categories as defined in `menu_category/seed/menu_category_data.py`.

### 2. Seed Menus
```bash
python manage.py seed_menu
```
This will create menu items and assign them to categories based on `menu/seed/menu_data.py`. Ensure categories are seeded first.

### 3. Seed Orders
```bash
python manage.py seed_order_data
```
This will generate realistic order and order item data for analytics and dashboard features. You can clear existing orders before seeding with:
```bash
python manage.py seed_order_data --clear
```

## API Endpoints
- Dashboards: `/api/dashboards-insights/`
- Graphs: `/api/graphs/`
- Orders: `/api/orders/`
- Order Items: `/api/order-items/`

(See source code for more endpoints and details.)

## Notes
- For development, SQLite is supported, but PostgreSQL is recommended for production.
- Data generation scripts are idempotent and safe to run multiple times.
- For analytics and dashboard features, ensure all seed steps are completed.

---
For any questions or issues, please open an issue or contact the maintainer.
