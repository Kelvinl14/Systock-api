"""Router para gerenciar lojas."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Store
from app.schemas.store import StoreCreate, StoreUpdate, StoreRead

router = APIRouter(prefix="/stores", tags=["stores"])


@router.get("", response_model=list[StoreRead])
def list_stores(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: str | None = None,
):
    """Lista todas as lojas com filtros opcionais."""
    query = db.query(Store)
    
    if name:
        query = query.filter(Store.name.ilike(f"%{name}%"))
    
    return query.offset(skip).limit(limit).all()

@router.get("/all", response_model=list[StoreRead])
def list_stores_all(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    name: str | None = None,
):
    """Lista todas as lojas sem limite com filtros opcionais."""
    query = db.query(Store)
    
    if name:
        query = query.filter(Store.name.ilike(f"%{name}%"))
    
    return query.offset(skip).all()


@router.get("/{store_id}", response_model=StoreRead)
def get_store(store_id: int, db: Session = Depends(get_db)):
    """Obtém uma loja pelo ID."""
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    return store


@router.post("", response_model=StoreRead, status_code=201)
def create_store(store: StoreCreate, db: Session = Depends(get_db)):
    """Cria uma nova loja."""
    # Validar unicidade de nome
    existing = db.query(Store).filter(Store.name == store.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Loja já existe")
    
    db_store = Store(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


@router.put("/{store_id}", response_model=StoreRead)
def update_store(
    store_id: int,
    store: StoreUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza uma loja."""
    db_store = db.query(Store).filter(Store.id == store_id).first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    
    update_data = store.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_store, field, value)
    
    db.commit()
    db.refresh(db_store)
    return db_store


@router.delete("/{store_id}", status_code=204)
def delete_store(store_id: int, db: Session = Depends(get_db)):
    """Deleta uma loja."""
    db_store = db.query(Store).filter(Store.id == store_id).first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    
    db.delete(db_store)
    db.commit()
