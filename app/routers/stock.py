"""Router para gerenciar estoque por loja."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import StockStore
from app.schemas.stock_store import StockStoreRead, StockStoreUpdate

router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("", response_model=list[StockStoreRead])
def list_stock(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    store_id: int | None = None,
    product_id: int | None = None,
):
    """Lista estoque com filtros opcionais."""
    query = db.query(StockStore)
    
    if store_id:
        query = query.filter(StockStore.store_id == store_id)
    
    if product_id:
        query = query.filter(StockStore.product_id == product_id)
    
    return query.offset(skip).limit(limit).all()


@router.get("/{stock_id}", response_model=StockStoreRead)
def get_stock(stock_id: int, db: Session = Depends(get_db)):
    """Obtém um registro de estoque pelo ID."""
    stock = db.query(StockStore).filter(StockStore.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    return stock


@router.get("/stores/{store_id}/products/{product_id}", response_model=StockStoreRead)
def get_stock_by_store_and_product(
    store_id: int,
    product_id: int,
    db: Session = Depends(get_db)
):
    """Obtém a quantidade de estoque para uma loja e produto específicos."""
    stock = db.query(StockStore).filter(
        StockStore.store_id == store_id,
        StockStore.product_id == product_id,
    ).first()
    
    if not stock:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    
    return stock


@router.put("/{stock_id}", response_model=StockStoreRead)
def update_stock(
    stock_id: int,
    stock: StockStoreUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um registro de estoque."""
    db_stock = db.query(StockStore).filter(StockStore.id == stock_id).first()
    if not db_stock:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    
    update_data = stock.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_stock, field, value)
    
    db.commit()
    db.refresh(db_stock)
    return db_stock


@router.delete("/{stock_id}", status_code=204)
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    """Deleta um registro de estoque."""
    db_stock = db.query(StockStore).filter(StockStore.id == stock_id).first()
    if not db_stock:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    
    db.delete(db_stock)
    db.commit()
