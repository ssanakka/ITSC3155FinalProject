from . import customers, menu_items, orders, order_items, payments, promotions, staff, reviews
from ..dependencies.database import Base, engine

from api.models.customers import Customer
from api.models.menu_items import MenuItem
from api.models.orders import Order
from api.models.order_items import OrderItem
from api.models.payments import Payment
from api.models.promotions import Promotion
from api.models.staff import Staff
from api.models.reviews import Review


def index():
    Base.metadata.create_all(bind=engine)
