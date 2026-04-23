# Food Delivery API

A REST API for a food delivery and ordering system built with **FastAPI**, **SQLAlchemy**, and **MySQL**.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | MySQL |
| Validation | Pydantic v2 |
| Testing | pytest (SQLite in-memory) |
| Server | Uvicorn |

---

## Database

**Database name:** `food_delivery_api`

| Table | Description |
|---|---|
| `customers` | Guest customer info — name, phone, address |
| `menu_items` | Food menu with category, ingredients, calories, and price |
| `orders` | Customer orders — takeout or delivery, status, tracking number, promo code |
| `order_items` | Individual food items within each order |
| `payments` | Payment records — method and status |
| `promotions` | Promo codes with discount percentages and expiration dates |
| `staff` | Staff members who manage orders |
| `reviews` | Customer ratings and comments on orders/dishes |

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/ssanakka/ITSC3155FinalProject.git
cd ITSC3155FinalProject
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up MySQL
```sql
CREATE DATABASE food_delivery_api;
```

Update credentials in `api/dependencies/config.py` if needed:
```python
class conf:
    db_host = "localhost"
    db_name = "food_delivery_api"
    db_port = 3306
    db_user = "root"
    db_password = "your_password"
```

### 4. Run the server
```bash
python3 -m uvicorn api.main:app --reload
```

Visit **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

---

## API Endpoints

### Customers
| Method | Endpoint | Description |
|---|---|---|
| GET | `/customers/` | List all customers |
| GET | `/customers/{id}` | Get a customer by ID |
| POST | `/customers/` | Register a guest customer |
| PUT | `/customers/{id}` | Update customer info |
| DELETE | `/customers/{id}` | Delete a customer |

### Menu Items
| Method | Endpoint | Description |
|---|---|---|
| GET | `/menu-items/` | List all items (filter by `?category=` or `?search=`) |
| GET | `/menu-items/{id}` | Get a menu item by ID |
| POST | `/menu-items/` | Add a new menu item |
| PUT | `/menu-items/{id}` | Update a menu item |
| DELETE | `/menu-items/{id}` | Delete a menu item |

### Orders
| Method | Endpoint | Description |
|---|---|---|
| GET | `/orders/` | List all orders (filter by `?start_date=` and `?end_date=`) |
| GET | `/orders/{id}` | Get an order by ID |
| GET | `/orders/track/{tracking_number}` | Track order status by tracking number |
| GET | `/orders/revenue?target_date=` | Get total revenue for a given day |
| POST | `/orders/` | Place a new order (takeout or delivery) |
| PUT | `/orders/{id}` | Update order status or details |
| DELETE | `/orders/{id}` | Delete an order |

### Order Items
| Method | Endpoint | Description |
|---|---|---|
| GET | `/order-items/` | List all order items |
| GET | `/order-items/{id}` | Get an order item by ID |
| POST | `/order-items/` | Add an item to an order |
| PUT | `/order-items/{id}` | Update quantity or price |
| DELETE | `/order-items/{id}` | Remove an item from an order |

### Payments
| Method | Endpoint | Description |
|---|---|---|
| GET | `/payments/` | List all payments |
| GET | `/payments/{id}` | Get a payment by ID |
| POST | `/payments/` | Process a payment |
| PUT | `/payments/{id}` | Update payment status |
| DELETE | `/payments/{id}` | Delete a payment record |

### Promotions
| Method | Endpoint | Description |
|---|---|---|
| GET | `/promotions/` | List all promo codes |
| GET | `/promotions/{id}` | Get a promo code by ID |
| POST | `/promotions/` | Create a promo code |
| PUT | `/promotions/{id}` | Update a promo code |
| DELETE | `/promotions/{id}` | Delete a promo code |

### Staff
| Method | Endpoint | Description |
|---|---|---|
| GET | `/staff/` | List all staff |
| GET | `/staff/{id}` | Get a staff member by ID |
| POST | `/staff/` | Add a staff member |
| PUT | `/staff/{id}` | Update staff details |
| DELETE | `/staff/{id}` | Remove a staff member |

### Reviews
| Method | Endpoint | Description |
|---|---|---|
| GET | `/reviews/` | List all reviews (filter by `?min_rating=`) |
| GET | `/reviews/{id}` | Get a review by ID |
| POST | `/reviews/` | Submit a review (rating 1–5) |
| PUT | `/reviews/{id}` | Update a review |
| DELETE | `/reviews/{id}` | Delete a review |

---

## Questions Addressed

### Staff Perspective
| Question | Endpoint |
|---|---|
| Create, update, or delete menu items? | `POST/PUT/DELETE /menu-items/` |
| View all orders? View a specific order? | `GET /orders/` and `GET /orders/{id}` |
| View orders within a date range? | `GET /orders/?start_date=&end_date=` |
| Total revenue for a given day? | `GET /orders/revenue?target_date=` |
| View complaints / low-rated dishes? | `GET /reviews/?min_rating=1` |
| Create and manage promo codes with expiration? | `POST/PUT /promotions/` |
| Search menu by food type / category? | `GET /menu-items/?category=vegetarian` |

### Customer Perspective
| Question | Endpoint |
|---|---|
| Place an order without signing up? | `POST /customers/` then `POST /orders/` |
| Pay for an order? | `POST /payments/` |
| Takeout or delivery? | `order_type` field in `POST /orders/` |
| Track order by tracking number? | `GET /orders/track/{tracking_number}` |
| Search for specific food types? | `GET /menu-items/?category=vegetarian` |
| Rate and review dishes? | `POST /reviews/` |
| Apply a promo code? | `promo_code` field in `POST /orders/` |

---

## Running Tests

```bash
python3 -m pytest api/tests/test_api.py -v
```

Expected output: **57 passed**

---

## 📁 Project Structure

```
softwaregroupproject/
├── requirements.txt
├── README.md
└── api/
    ├── main.py
    ├── dependencies/
    │   ├── config.py
    │   └── database.py
    ├── models/
    │   ├── model_loader.py
    │   ├── customers.py
    │   ├── menu_items.py
    │   ├── orders.py
    │   ├── order_items.py
    │   ├── payments.py
    │   ├── promotions.py
    │   ├── staff.py
    │   └── reviews.py
    ├── schemas/
    │   ├── customers.py
    │   ├── menu_items.py
    │   ├── orders.py
    │   ├── order_items.py
    │   ├── payments.py
    │   ├── promotions.py
    │   ├── staff.py
    │   └── reviews.py
    ├── controllers/
    │   ├── customers.py
    │   ├── menu_items.py
    │   ├── orders.py
    │   ├── order_items.py
    │   ├── payments.py
    │   ├── promotions.py
    │   ├── staff.py
    │   └── reviews.py
    ├── routers/
    │   ├── index.py
    │   ├── customers.py
    │   ├── menu_items.py
    │   ├── orders.py
    │   ├── order_items.py
    │   ├── payments.py
    │   ├── promotions.py
    │   ├── staff.py
    │   └── reviews.py
    └── tests/
        └── test_api.py
```

---

## Team Members

- Sumanth Sanakkayala
- Ananya Patchigolla
- Pearl Patel
- Mahad Duale

---

## Demo Video

[Link to recorded presentation]
