"""
Tests for the Food Delivery API.
Uses SQLite in-memory — no MySQL connection required.
Run from project root with: python3 -m pytest api/tests/test_api.py -v
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.dependencies.database import Base, get_db
from api.main import app

SQLALCHEMY_TEST_URL = "sqlite:///./test_food_delivery.db"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_customer(name="John Doe", phone="704-555-0001", address="123 Main St", email=None):
    payload = {"name": name, "phone": phone, "address": address}
    if email:
        payload["email"] = email
    return client.post("/customers/", json=payload).json()


def make_menu_item(name="Burger", category="Mains", price=9.99):
    return client.post("/menu-items/", json={
        "name": name, "category": category, "price": price,
        "ingredients": "Beef, Lettuce, Tomato", "calories": 650
    }).json()


def make_order(customer_id, order_type="takeout"):
    return client.post("/orders/", json={
        "customer_id": customer_id, "order_type": order_type
    }).json()


# ── Customer Tests ────────────────────────────────────────────────────────────

class TestCustomers:

    def test_create_customer(self):
        response = client.post("/customers/", json={
            "name": "Jane Doe", "phone": "555-1234", "address": "456 Oak Ave"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Jane Doe"
        assert data["phone"] == "555-1234"
        assert "id" in data

    def test_get_all_customers(self):
        make_customer("Alice", "555-0001", "1 St", "alice@test.com")
        make_customer("Bob", "555-0002", "2 St", "bob@test.com")
        response = client.get("/customers/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_customer_by_id(self):
        c = make_customer()
        response = client.get(f"/customers/{c['id']}")
        assert response.status_code == 200
        assert response.json()["name"] == "John Doe"

    def test_get_customer_not_found(self):
        assert client.get("/customers/9999").status_code == 404

    def test_update_customer(self):
        c = make_customer()
        response = client.put(f"/customers/{c['id']}", json={"address": "999 New St"})
        assert response.status_code == 200
        assert response.json()["address"] == "999 New St"

    def test_delete_customer(self):
        c = make_customer()
        assert client.delete(f"/customers/{c['id']}").status_code == 204
        assert client.get(f"/customers/{c['id']}").status_code == 404


# ── Menu Item Tests ───────────────────────────────────────────────────────────

class TestMenuItems:

    def test_create_menu_item(self):
        response = client.post("/menu-items/", json={
            "name": "Pizza", "category": "Mains", "price": 12.99,
            "ingredients": "Dough, Cheese, Tomato", "calories": 800
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Pizza"
        assert data["price"] == 12.99

    def test_get_all_menu_items(self):
        make_menu_item("Burger", "Mains", 9.99)
        make_menu_item("Fries", "Sides", 3.99)
        response = client.get("/menu-items/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_menu_item_by_id(self):
        item = make_menu_item()
        response = client.get(f"/menu-items/{item['id']}")
        assert response.status_code == 200
        assert response.json()["name"] == "Burger"

    def test_get_menu_item_not_found(self):
        assert client.get("/menu-items/9999").status_code == 404

    def test_update_menu_item(self):
        item = make_menu_item()
        response = client.put(f"/menu-items/{item['id']}", json={"price": 11.99})
        assert response.status_code == 200
        assert response.json()["price"] == 11.99

    def test_delete_menu_item(self):
        item = make_menu_item()
        assert client.delete(f"/menu-items/{item['id']}").status_code == 204
        assert client.get(f"/menu-items/{item['id']}").status_code == 404

    def test_duplicate_name_rejected(self):
        make_menu_item("Burger", "Mains", 9.99)
        response = client.post("/menu-items/", json={"name": "Burger", "category": "Mains", "price": 10.99})
        assert response.status_code == 400


# ── Order Tests ───────────────────────────────────────────────────────────────

class TestOrders:

    def test_create_order(self):
        c = make_customer()
        response = client.post("/orders/", json={
            "customer_id": c["id"], "order_type": "delivery"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["order_type"] == "delivery"
        assert data["status"] == "pending"
        assert "tracking_number" in data
        assert data["tracking_number"].startswith("TRK-")

    def test_get_all_orders(self):
        c = make_customer()
        make_order(c["id"])
        make_order(c["id"], "delivery")
        response = client.get("/orders/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_order_by_id(self):
        c = make_customer()
        order = make_order(c["id"])
        response = client.get(f"/orders/{order['id']}")
        assert response.status_code == 200

    def test_get_order_not_found(self):
        assert client.get("/orders/9999").status_code == 404

    def test_update_order_status(self):
        c = make_customer()
        order = make_order(c["id"])
        response = client.put(f"/orders/{order['id']}", json={"status": "preparing"})
        assert response.status_code == 200
        assert response.json()["status"] == "preparing"

    def test_delete_order(self):
        c = make_customer()
        order = make_order(c["id"])
        assert client.delete(f"/orders/{order['id']}").status_code == 204
        assert client.get(f"/orders/{order['id']}").status_code == 404

    def test_order_with_promo_code(self):
        c = make_customer()
        response = client.post("/orders/", json={
            "customer_id": c["id"], "order_type": "takeout", "promo_code": "SAVE10"
        })
        assert response.status_code == 200
        assert response.json()["promo_code"] == "SAVE10"


# ── Order Item Tests ──────────────────────────────────────────────────────────

class TestOrderItems:

    def test_create_order_item(self):
        c = make_customer()
        order = make_order(c["id"])
        item = make_menu_item()
        response = client.post("/order-items/", json={
            "order_id": order["id"], "menu_item_id": item["id"],
            "quantity": 2, "price": 9.99
        })
        assert response.status_code == 200
        assert response.json()["quantity"] == 2

    def test_get_all_order_items(self):
        c = make_customer()
        order = make_order(c["id"])
        item = make_menu_item()
        client.post("/order-items/", json={"order_id": order["id"], "menu_item_id": item["id"], "quantity": 1, "price": 9.99})
        response = client.get("/order-items/")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_order_item_by_id(self):
        c = make_customer()
        order = make_order(c["id"])
        item = make_menu_item()
        created = client.post("/order-items/", json={"order_id": order["id"], "menu_item_id": item["id"], "quantity": 1, "price": 9.99}).json()
        response = client.get(f"/order-items/{created['id']}")
        assert response.status_code == 200

    def test_update_order_item(self):
        c = make_customer()
        order = make_order(c["id"])
        item = make_menu_item()
        created = client.post("/order-items/", json={"order_id": order["id"], "menu_item_id": item["id"], "quantity": 1, "price": 9.99}).json()
        response = client.put(f"/order-items/{created['id']}", json={"quantity": 3})
        assert response.status_code == 200
        assert response.json()["quantity"] == 3

    def test_delete_order_item(self):
        c = make_customer()
        order = make_order(c["id"])
        item = make_menu_item()
        created = client.post("/order-items/", json={"order_id": order["id"], "menu_item_id": item["id"], "quantity": 1, "price": 9.99}).json()
        assert client.delete(f"/order-items/{created['id']}").status_code == 204


# ── Payment Tests ─────────────────────────────────────────────────────────────

class TestPayments:

    def test_create_payment(self):
        c = make_customer()
        order = make_order(c["id"])
        response = client.post("/payments/", json={
            "order_id": order["id"], "customer_id": c["id"],
            "payment_method": "credit_card", "amount": 19.99
        })
        assert response.status_code == 200
        data = response.json()
        assert data["payment_method"] == "credit_card"
        assert data["payment_status"] == "pending"

    def test_get_all_payments(self):
        c = make_customer()
        order = make_order(c["id"])
        client.post("/payments/", json={"order_id": order["id"], "customer_id": c["id"], "payment_method": "cash", "amount": 10.0})
        response = client.get("/payments/")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_payment_by_id(self):
        c = make_customer()
        order = make_order(c["id"])
        p = client.post("/payments/", json={"order_id": order["id"], "customer_id": c["id"], "payment_method": "paypal", "amount": 15.0}).json()
        response = client.get(f"/payments/{p['id']}")
        assert response.status_code == 200

    def test_update_payment_status(self):
        c = make_customer()
        order = make_order(c["id"])
        p = client.post("/payments/", json={"order_id": order["id"], "customer_id": c["id"], "payment_method": "debit_card", "amount": 25.0}).json()
        response = client.put(f"/payments/{p['id']}", json={"payment_status": "completed"})
        assert response.status_code == 200
        assert response.json()["payment_status"] == "completed"

    def test_delete_payment(self):
        c = make_customer()
        order = make_order(c["id"])
        p = client.post("/payments/", json={"order_id": order["id"], "customer_id": c["id"], "payment_method": "apple_pay", "amount": 30.0}).json()
        assert client.delete(f"/payments/{p['id']}").status_code == 204


# ── Promotion Tests ───────────────────────────────────────────────────────────

class TestPromotions:

    def test_create_promotion(self):
        response = client.post("/promotions/", json={
            "promo_code": "SAVE10", "description": "10% off", "discount_percent": 10.0
        })
        assert response.status_code == 200
        data = response.json()
        assert data["promo_code"] == "SAVE10"
        assert data["is_active"] is True

    def test_get_all_promotions(self):
        client.post("/promotions/", json={"promo_code": "DEAL1", "discount_percent": 5.0})
        client.post("/promotions/", json={"promo_code": "DEAL2", "discount_percent": 15.0})
        response = client.get("/promotions/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_promotion_by_id(self):
        p = client.post("/promotions/", json={"promo_code": "HALF50", "discount_percent": 50.0}).json()
        response = client.get(f"/promotions/{p['id']}")
        assert response.status_code == 200
        assert response.json()["promo_code"] == "HALF50"

    def test_get_promotion_not_found(self):
        assert client.get("/promotions/9999").status_code == 404

    def test_update_promotion(self):
        p = client.post("/promotions/", json={"promo_code": "OLD20", "discount_percent": 20.0}).json()
        response = client.put(f"/promotions/{p['id']}", json={"is_active": False})
        assert response.status_code == 200
        assert response.json()["is_active"] is False

    def test_delete_promotion(self):
        p = client.post("/promotions/", json={"promo_code": "DEL30", "discount_percent": 30.0}).json()
        assert client.delete(f"/promotions/{p['id']}").status_code == 204
        assert client.get(f"/promotions/{p['id']}").status_code == 404

    def test_duplicate_promo_code_rejected(self):
        client.post("/promotions/", json={"promo_code": "SAME", "discount_percent": 10.0})
        response = client.post("/promotions/", json={"promo_code": "SAME", "discount_percent": 20.0})
        assert response.status_code == 400


# ── Staff Tests ───────────────────────────────────────────────────────────────

class TestStaff:

    def test_create_staff(self):
        response = client.post("/staff/", json={
            "name": "Maria", "role": "Manager", "email": "maria@food.com", "phone": "555-9000"
        })
        assert response.status_code == 200
        assert response.json()["role"] == "Manager"

    def test_get_all_staff(self):
        client.post("/staff/", json={"name": "Ana", "role": "Cook", "email": "ana@food.com"})
        client.post("/staff/", json={"name": "Tom", "role": "Driver", "email": "tom@food.com"})
        response = client.get("/staff/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_staff_by_id(self):
        s = client.post("/staff/", json={"name": "Lee", "role": "Cashier", "email": "lee@food.com"}).json()
        response = client.get(f"/staff/{s['id']}")
        assert response.status_code == 200
        assert response.json()["name"] == "Lee"

    def test_get_staff_not_found(self):
        assert client.get("/staff/9999").status_code == 404

    def test_update_staff(self):
        s = client.post("/staff/", json={"name": "Kim", "role": "Waiter", "email": "kim@food.com"}).json()
        response = client.put(f"/staff/{s['id']}", json={"role": "Supervisor"})
        assert response.status_code == 200
        assert response.json()["role"] == "Supervisor"

    def test_delete_staff(self):
        s = client.post("/staff/", json={"name": "Del", "role": "Driver", "email": "del@food.com"}).json()
        assert client.delete(f"/staff/{s['id']}").status_code == 204
        assert client.get(f"/staff/{s['id']}").status_code == 404


# ── Review Tests ──────────────────────────────────────────────────────────────

class TestReviews:

    def test_create_review(self):
        c = make_customer()
        order = make_order(c["id"])
        item = make_menu_item()
        response = client.post("/reviews/", json={
            "customer_id": c["id"], "order_id": order["id"],
            "menu_item_id": item["id"], "rating": 5, "comment": "Excellent!"
        })
        assert response.status_code == 200
        assert response.json()["rating"] == 5

    def test_get_all_reviews(self):
        c = make_customer()
        order = make_order(c["id"])
        client.post("/reviews/", json={"customer_id": c["id"], "order_id": order["id"], "rating": 4})
        response = client.get("/reviews/")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_review_by_id(self):
        c = make_customer()
        order = make_order(c["id"])
        r = client.post("/reviews/", json={"customer_id": c["id"], "order_id": order["id"], "rating": 3}).json()
        response = client.get(f"/reviews/{r['id']}")
        assert response.status_code == 200

    def test_get_review_not_found(self):
        assert client.get("/reviews/9999").status_code == 404

    def test_update_review(self):
        c = make_customer()
        order = make_order(c["id"])
        r = client.post("/reviews/", json={"customer_id": c["id"], "order_id": order["id"], "rating": 2}).json()
        response = client.put(f"/reviews/{r['id']}", json={"rating": 5, "comment": "Changed my mind!"})
        assert response.status_code == 200
        assert response.json()["rating"] == 5

    def test_delete_review(self):
        c = make_customer()
        order = make_order(c["id"])
        r = client.post("/reviews/", json={"customer_id": c["id"], "order_id": order["id"], "rating": 1}).json()
        assert client.delete(f"/reviews/{r['id']}").status_code == 204

    def test_invalid_rating_rejected(self):
        c = make_customer()
        order = make_order(c["id"])
        response = client.post("/reviews/", json={"customer_id": c["id"], "order_id": order["id"], "rating": 6})
        assert response.status_code == 422

    def test_filter_reviews_by_min_rating(self):
        c = make_customer()
        o1 = make_order(c["id"])
        o2 = make_order(c["id"])
        client.post("/reviews/", json={"customer_id": c["id"], "order_id": o1["id"], "rating": 1})
        client.post("/reviews/", json={"customer_id": c["id"], "order_id": o2["id"], "rating": 5})
        response = client.get("/reviews/?min_rating=4")
        assert response.status_code == 200
        assert all(r["rating"] >= 4 for r in response.json())


# ── Order Tracking & Date Filter Tests ───────────────────────────────────────

class TestOrderExtras:

    def test_track_order_by_tracking_number(self):
        c = make_customer()
        order = make_order(c["id"])
        tracking = order["tracking_number"]
        response = client.get(f"/orders/track/{tracking}")
        assert response.status_code == 200
        assert response.json()["tracking_number"] == tracking

    def test_track_order_not_found(self):
        assert client.get("/orders/track/TRK-INVALID").status_code == 404

    def test_revenue_endpoint(self):
        response = client.get("/orders/revenue")
        assert response.status_code == 200
        assert "total_revenue" in response.json()
        assert "date" in response.json()

    def test_menu_item_search_by_category(self):
        client.post("/menu-items/", json={"name": "Veggie Wrap", "category": "vegetarian", "price": 8.99})
        client.post("/menu-items/", json={"name": "Steak", "category": "mains", "price": 24.99})
        response = client.get("/menu-items/?category=vegetarian")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Veggie Wrap"

    def test_menu_item_search_by_ingredient(self):
        client.post("/menu-items/", json={"name": "Tofu Bowl", "category": "vegetarian", "price": 10.99, "ingredients": "tofu, rice, soy sauce"})
        response = client.get("/menu-items/?search=tofu")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_promotion_with_expiration_date(self):
        response = client.post("/promotions/", json={
            "promo_code": "EXPIRE10", "discount_percent": 10.0,
            "expiration_date": "2026-12-31"
        })
        assert response.status_code == 200
        assert response.json()["expiration_date"] == "2026-12-31"
