from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..controllers import menu_items as controller
from ..schemas import menu_items as schema
from ..dependencies.database import get_db
from ..models.menu_items import MenuItem

router = APIRouter(tags=['Menu Items'], prefix="/menu-items")


@router.post("/", response_model=schema.MenuItem)
def create(request: schema.MenuItemCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.MenuItem])
def read_all(
    category: Optional[str] = Query(None, description="Filter by category (e.g. vegetarian, pizza, burgers)"),
    search: Optional[str] = Query(None, description="Search by name or ingredient"),
    db: Session = Depends(get_db)
):
    """Get all menu items. Filter by category or search by name/ingredient."""
    query = db.query(MenuItem)
    if category:
        query = query.filter(MenuItem.category.ilike(f"%{category}%"))
    if search:
        query = query.filter(
            MenuItem.name.ilike(f"%{search}%") |
            MenuItem.ingredients.ilike(f"%{search}%")
        )
    return query.all()


@router.get("/{item_id}", response_model=schema.MenuItem)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.MenuItem)
def update(item_id: int, request: schema.MenuItemUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
