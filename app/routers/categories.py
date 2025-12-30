"""Router para gerenciar categorias."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryRead

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryRead])
def list_categories(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: str | None = None,
):
    """Lista todas as categorias com filtros opcionais."""
    query = db.query(Category)
    
    if name:
        query = query.filter(Category.name.ilike(f"%{name}%"))
    
    return query.offset(skip).limit(limit).all()

@router.get("/all", response_model=list[CategoryRead])
def list_categories_all(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    name: str | None = None,
):
    """Lista todas as categorias sem limite com filtros opcionais."""
    query = db.query(Category)
    
    if name:
        query = query.filter(Category.name.ilike(f"%{name}%"))
    
    return query.offset(skip).all()


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Obtém uma categoria pelo ID."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category


@router.post("", response_model=CategoryRead, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Cria uma nova categoria."""
    # Validar unicidade de nome
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Categoria já existe")
    
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza uma categoria."""
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    update_data = category.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Deleta uma categoria."""
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    db.delete(db_category)
    db.commit()
