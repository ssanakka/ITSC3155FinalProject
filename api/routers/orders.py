from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import date
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import get_db
from ..models.orders import Order

router = APIRouter(tags=['Orders'], prefix="/orders")


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/revenue", response_model=dict)
def get_revenue(
    target_date: Optional[date] = Query(None, description="Date (YYYY-MM-DD). Defaults to today."),
    db: Session = Depends(get_db)
):
    """Get total revenue from food sales for a given day."""
    from datetime import date as date_type
    day = target_date or date_type.today()
    result = db.query(func.sum(Order.total_price)).filter(
        Order.created_at >= str(day),
        Order.created_at <= f"{day} 23:59:59"
    ).scalar()
    return {"date": str(day), "total_revenue": round(result or 0.0, 2)}


@router.get("/track/{tracking_number}", response_model=schema.Order)
def track_order(tracking_number: str, db: Session = Depends(get_db)):
    """Track an order status by tracking number."""
    order = db.query(Order).filter(Order.tracking_number == tracking_number).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracking number not found!")
    return order


@router.get("/", response_model=list[schema.Order])
def read_all(
    start_date: Optional[date] = Query(None, description="Filter from this date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter up to this date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get all orders. Optionally filter by date range."""
    query = db.query(Order)
    if start_date:
        query = query.filter(Order.created_at >= str(start_date))
    if end_date:
        query = query.filter(Order.created_at <= f"{end_date} 23:59:59")
    return query.all()


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
