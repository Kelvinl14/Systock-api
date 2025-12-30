"""Router para gerenciar movimentações de estoque."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import StockMovement
from app.schemas.stock_movement import StockMovementRead

router = APIRouter(prefix="/movements", tags=["movements"])


@router.get("", response_model=list[StockMovementRead])
def list_movements(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    product_id: int | None = None,
    store_id: int | None = None,
    movement_type: str | None = None,
    reference_type: str | None = None,
):
    """Lista movimentações de estoque com filtros opcionais."""
    query = db.query(StockMovement)
    
    if product_id:
        query = query.filter(StockMovement.product_id == product_id)
    
    if store_id:
        query = query.filter(StockMovement.store_id == store_id)
    
    if movement_type:
        query = query.filter(StockMovement.movement_type == movement_type)
    
    if reference_type:
        query = query.filter(StockMovement.reference_type == reference_type)
    
    return query.order_by(StockMovement.movement_date.desc()).offset(skip).limit(limit).all()

@router.get("/all", response_model=list[StockMovementRead])
def list_movements_all(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    product_id: int | None = None,
    store_id: int | None = None,
    movement_type: str | None = None,
    reference_type: str | None = None,
):
    """Lista movimentações de estoque sem limite com filtros opcionais."""
    query = db.query(StockMovement)
    
    if product_id:
        query = query.filter(StockMovement.product_id == product_id)
    
    if store_id:
        query = query.filter(StockMovement.store_id == store_id)
    
    if movement_type:
        query = query.filter(StockMovement.movement_type == movement_type)
    
    if reference_type:
        query = query.filter(StockMovement.reference_type == reference_type)
    
    return query.order_by(StockMovement.movement_date.desc()).offset(skip).all()


@router.get("/{movement_id}", response_model=StockMovementRead)
def get_movement(movement_id: int, db: Session = Depends(get_db)):
    """Obtém uma movimentação de estoque pelo ID."""
    movement = db.query(StockMovement).filter(StockMovement.id == movement_id).first()
    if not movement:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    return movement


@router.get("/by-reference/{reference_type}/{reference_id}", response_model=list[StockMovementRead])
def get_movements_by_reference(
    reference_type: str,
    reference_id: int,
    db: Session = Depends(get_db)
):
    """Obtém todas as movimentações relacionadas a uma referência."""
    movements = db.query(StockMovement).filter(
        StockMovement.reference_type == reference_type,
        StockMovement.reference_id == reference_id,
    ).order_by(StockMovement.movement_date.desc()).all()
    
    return movements
