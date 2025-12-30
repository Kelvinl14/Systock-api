"""Router para gerenciar vendas."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Sale, SaleItem
from app.schemas.sale import SaleCreate, SaleRead
from app.services.sales_service import SalesService

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("", response_model=list[SaleRead])
def list_sales(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    client_id: int | None = None,
    store_id: int | None = None,
    status: str | None = None,
):
    """Lista vendas com filtros opcionais."""
    query = db.query(Sale)
    
    if client_id:
        query = query.filter(Sale.client_id == client_id)
    
    if store_id:
        query = query.filter(Sale.store_id == store_id)
    
    if status:
        query = query.filter(Sale.status == status)
    
    return query.offset(skip).limit(limit).all()

@router.get("/all", response_model=list[SaleRead])
def list_sales_all(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    client_id: int | None = None,
    store_id: int | None = None,
    status: str | None = None,
):
    """Lista vendas sem limite com filtros opcionais."""
    query = db.query(Sale)
    
    if client_id:
        query = query.filter(Sale.client_id == client_id)
    
    if store_id:
        query = query.filter(Sale.store_id == store_id)
    
    if status:
        query = query.filter(Sale.status == status)
    
    return query.offset(skip).all()


@router.get("/{sale_id}", response_model=SaleRead)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    """Obtém uma venda pelo ID."""
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return sale


@router.post("", response_model=SaleRead, status_code=201)
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db)
):
    """
    Cria uma nova venda com validação de estoque e registro automático de movimentação.
    
    COMENTÁRIO DE AUDITORIA: Esta rota implementa a lógica transacional completa:
    1. Valida se há estoque suficiente na loja para todos os itens
    2. Cria o cabeçalho da venda (Sale)
    3. Cria todos os itens (SaleItem)
    4. Registra as movimentações de estoque (movement_type='sale') e atualiza StockStore
    
    Se houver estoque insuficiente, retorna 400 com mensagem clara.
    Se qualquer erro ocorrer após a criação dos itens, a transação é revertida.
    """
    try:
        # Validar estoque
        items_list = [item.dict() for item in sale.items]
        is_valid, error_msg = SalesService.validate_sale_items_stock(
            db, sale.store_id, items_list
        )
        
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # Criar venda
        db_sale = Sale(
            client_id=sale.client_id,
            store_id=sale.store_id,
            sale_date=sale.sale_date,
            delivery_type=sale.delivery_type,
            tracking_code=sale.tracking_code,
            status=sale.status,
            predicted_delivery=sale.predicted_delivery,
            delivered_at=sale.delivered_at,
            total_value=sale.total_value,
        )
        db.add(db_sale)
        db.flush()

        # Criar itens
        for item_data in sale.items:
            db_item = SaleItem(
                sale_id=db_sale.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                total_price=item_data.total_price,
                removed_at=item_data.removed_at,
            )
            db.add(db_item)
        db.flush()

        # Registrar movimentações de estoque
        SalesService.register_sale_movements(db, db_sale.id)

        # Commit da transação
        db.commit()
        db.refresh(db_sale)
        return db_sale

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar venda: {str(e)}")


@router.put("/{sale_id}", response_model=SaleRead)
def update_sale(
    sale_id: int,
    status: str = Query(..., description="Novo status da venda"),
    db: Session = Depends(get_db)
):
    """Atualiza o status de uma venda."""
    db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    db_sale.status = status
    db.commit()
    db.refresh(db_sale)
    return db_sale


@router.delete("/{sale_id}", status_code=204)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    """Deleta uma venda."""
    db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    # Deletar itens associados
    db.query(SaleItem).filter(SaleItem.sale_id == sale_id).delete()
    
    db.delete(db_sale)
    db.commit()
