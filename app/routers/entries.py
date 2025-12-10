"""Router para gerenciar entradas de produtos."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import ProductEntry, ProductEntryItem
from app.schemas.product_entry import ProductEntryCreate, ProductEntryRead
from app.services.entries_service import EntriesService

router = APIRouter(prefix="/entries", tags=["entries"])


@router.get("", response_model=list[ProductEntryRead])
def list_entries(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    supplier_id: int | None = None,
    status: str | None = None,
):
    """Lista entradas de produtos com filtros opcionais."""
    query = db.query(ProductEntry)
    
    if supplier_id:
        query = query.filter(ProductEntry.supplier_id == supplier_id)
    
    if status:
        query = query.filter(ProductEntry.status == status)
    
    return query.offset(skip).limit(limit).all()


@router.get("/{entry_id}", response_model=ProductEntryRead)
def get_entry(entry_id: int, db: Session = Depends(get_db)):
    """Obtém uma entrada de produtos pelo ID."""
    entry = db.query(ProductEntry).filter(ProductEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entrada não encontrada")
    return entry


@router.post("", response_model=ProductEntryRead, status_code=201)
def create_entry(
    entry: ProductEntryCreate,
    store_id: int = Query(1, description="ID da loja para registrar o estoque"),
    db: Session = Depends(get_db)
):
    """
    Cria uma nova entrada de produtos com registro automático de movimentação de estoque.
    
    COMENTÁRIO DE AUDITORIA: Esta rota implementa a lógica transacional completa:
    1. Cria o cabeçalho da entrada (ProductEntry)
    2. Cria todos os itens (ProductEntryItem)
    3. Registra as movimentações de estoque (StockMovement) e atualiza StockStore
    
    Se qualquer erro ocorrer após a criação dos itens, a transação é revertida
    e nenhuma movimentação é registrada, garantindo a integridade dos dados.
    """
    try:
        # Criar entrada
        db_entry = ProductEntry(
            supplier_id=entry.supplier_id,
            entry_date=entry.entry_date,
            invoice_number=entry.invoice_number,
            total_value=entry.total_value,
            status=entry.status,
        )
        db.add(db_entry)
        db.flush()

        # Criar itens
        for item_data in entry.items:
            db_item = ProductEntryItem(
                product_entry_id=db_entry.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                total_price=item_data.total_price,
                lot_number=item_data.lot_number,
                expiration_date=item_data.expiration_date,
                received_at=item_data.received_at,
            )
            db.add(db_item)
        db.flush()

        # Registrar movimentações de estoque
        EntriesService.register_entry_movements(db, db_entry.id, store_id)

        # Commit da transação
        db.commit()
        db.refresh(db_entry)
        return db_entry

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar entrada: {str(e)}")


@router.put("/{entry_id}", response_model=ProductEntryRead)
def update_entry(
    entry_id: int,
    status: str = Query(..., description="Novo status da entrada"),
    db: Session = Depends(get_db)
):
    """Atualiza o status de uma entrada de produtos."""
    db_entry = db.query(ProductEntry).filter(ProductEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entrada não encontrada")
    
    db_entry.status = status
    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.delete("/{entry_id}", status_code=204)
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    """Deleta uma entrada de produtos."""
    db_entry = db.query(ProductEntry).filter(ProductEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entrada não encontrada")
    
    # Deletar itens associados
    db.query(ProductEntryItem).filter(
        ProductEntryItem.product_entry_id == entry_id
    ).delete()
    
    db.delete(db_entry)
    db.commit()
