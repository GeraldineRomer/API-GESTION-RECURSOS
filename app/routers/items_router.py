from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.dependencies import get_current_user
from app import models, schemas

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=schemas.ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item_data: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),  # ← ruta protegida
):
    """Crea un item asociado al usuario autenticado."""
    new_item = models.Item(
        title=item_data.title,
        description=item_data.description,
        owner_id=current_user.id,
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get("/", response_model=List[schemas.ItemResponse])
def list_my_items(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Devuelve solo los items del usuario autenticado, no los de todos."""
    return db.query(models.Item).filter(models.Item.owner_id == current_user.id).all()


@router.get("/{item_id}", response_model=schemas.ItemResponse)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    item = db.query(models.Item).filter(
        models.Item.id == item_id,
        models.Item.owner_id == current_user.id,
    ).first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")

    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    item = db.query(models.Item).filter(
        models.Item.id == item_id,
        models.Item.owner_id == current_user.id,
    ).first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")

    db.delete(item)
    db.commit()
