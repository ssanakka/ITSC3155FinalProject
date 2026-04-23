from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..controllers import reviews as controller
from ..schemas import reviews as schema
from ..dependencies.database import get_db
from ..models.reviews import Review

router = APIRouter(tags=['Reviews'], prefix="/reviews")


@router.post("/", response_model=schema.Review)
def create(request: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Review])
def read_all(
    min_rating: Optional[int] = Query(None, description="Filter by minimum rating (1-5)"),
    db: Session = Depends(get_db)
):
    """Get all reviews. Staff can filter by min_rating to find complaints (e.g. min_rating=1)."""
    query = db.query(Review)
    if min_rating is not None:
        query = query.filter(Review.rating >= min_rating)
    return query.all()


@router.get("/{item_id}", response_model=schema.Review)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Review)
def update(item_id: int, request: schema.ReviewUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
