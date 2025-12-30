"""Router para gerenciar clientes."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Client
from app.schemas.client import ClientCreate, ClientUpdate, ClientRead

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=list[ClientRead])
def list_clients(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: str | None = None,
):
    """Lista todos os clientes com filtros opcionais."""
    query = db.query(Client)
    
    if name:
        query = query.filter(Client.name.ilike(f"%{name}%"))
    
    return query.offset(skip).limit(limit).all()

@router.get("/all", response_model=list[ClientRead])
def list_clients_all(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    name: str | None = None,
):
    """Lista todos os clientes sem limite com filtros opcionais."""
    query = db.query(Client)
    
    if name:
        query = query.filter(Client.name.ilike(f"%{name}%"))
    
    return query.offset(skip).all()


@router.get("/{client_id}", response_model=ClientRead)
def get_client(client_id: int, db: Session = Depends(get_db)):
    """Obtém um cliente pelo ID."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client


@router.post("", response_model=ClientRead, status_code=201)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    """Cria um novo cliente."""
    # Validar unicidade de CPF/CNPJ e email
    existing = db.query(Client).filter(
        (Client.cpf_cnpj == client.cpf_cnpj) | (Client.email == client.email)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail="CPF/CNPJ ou email já cadastrado"
        )
    
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@router.put("/{client_id}", response_model=ClientRead)
def update_client(
    client_id: int,
    client: ClientUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um cliente."""
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    update_data = client.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_client, field, value)
    
    db.commit()
    db.refresh(db_client)
    return db_client


@router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """Deleta um cliente."""
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    db.delete(db_client)
    db.commit()
