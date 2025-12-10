"""Router para gerenciar transportadoras."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Carrier
from app.schemas.carrier import CarrierCreate, CarrierUpdate, CarrierRead

router = APIRouter(prefix="/carriers", tags=["carriers"])


@router.get("", response_model=list[CarrierRead])
def list_carriers(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: str | None = None,
):
    """Lista todas as transportadoras com filtros opcionais."""
    query = db.query(Carrier)
    
    if name:
        query = query.filter(Carrier.name.ilike(f"%{name}%"))
    
    return query.offset(skip).limit(limit).all()


@router.get("/{carrier_id}", response_model=CarrierRead)
def get_carrier(carrier_id: int, db: Session = Depends(get_db)):
    """Obtém uma transportadora pelo ID."""
    carrier = db.query(Carrier).filter(Carrier.id == carrier_id).first()
    if not carrier:
        raise HTTPException(status_code=404, detail="Transportadora não encontrada")
    return carrier


@router.post("", response_model=CarrierRead, status_code=201)
def create_carrier(carrier: CarrierCreate, db: Session = Depends(get_db)):
    """Cria uma nova transportadora."""
    # Validar unicidade de nome
    existing = db.query(Carrier).filter(Carrier.name == carrier.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Transportadora já existe")
    
    db_carrier = Carrier(**carrier.dict())
    db.add(db_carrier)
    db.commit()
    db.refresh(db_carrier)
    return db_carrier


@router.put("/{carrier_id}", response_model=CarrierRead)
def update_carrier(
    carrier_id: int,
    carrier: CarrierUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza uma transportadora."""
    db_carrier = db.query(Carrier).filter(Carrier.id == carrier_id).first()
    if not db_carrier:
        raise HTTPException(status_code=404, detail="Transportadora não encontrada")
    
    update_data = carrier.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_carrier, field, value)
    
    db.commit()
    db.refresh(db_carrier)
    return db_carrier


@router.delete("/{carrier_id}", status_code=204)
def delete_carrier(carrier_id: int, db: Session = Depends(get_db)):
    """Deleta uma transportadora."""
    db_carrier = db.query(Carrier).filter(Carrier.id == carrier_id).first()
    if not db_carrier:
        raise HTTPException(status_code=404, detail="Transportadora não encontrada")
    
    db.delete(db_carrier)
    db.commit()
