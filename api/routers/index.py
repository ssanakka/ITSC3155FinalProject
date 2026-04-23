from . import customers, menu_items, orders, order_items, payments, promotions, staff, reviews


def load_routes(app):
    app.include_router(customers.router)
    app.include_router(menu_items.router)
    app.include_router(orders.router)
    app.include_router(order_items.router)
    app.include_router(payments.router)
    app.include_router(promotions.router)
    app.include_router(staff.router)
    app.include_router(reviews.router)
