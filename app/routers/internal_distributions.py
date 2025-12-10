"""Router para gerenciar distribuições internas entre lojas."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import InternalDistribution, InternalDistributionItem
from app.schemas.internal_distribution import InternalDistributionCreate, InternalDistributionRead
from app.services.distributions_service import DistributionsService

router = APIRouter(prefix="/internal-distributions", tags=["internal-distributions"])


@router.get("", response_model=list[InternalDistributionRead])
def list_distributions(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    from_store_id: int | None = None,
    to_store_id: int | None = None,
    status: str | None = None,
):
    """Lista distribuições internas com filtros opcionais."""
    query = db.query(InternalDistribution)
    
    if from_store_id:
        query = query.filter(InternalDistribution.from_store_id == from_store_id)
    
    if to_store_id:
        query = query.filter(InternalDistribution.to_store_id == to_store_id)
    
    if status:
        query = query.filter(InternalDistribution.status == status)
    
    return query.offset(skip).limit(limit).all()


@router.get("/{distribution_id}", response_model=InternalDistributionRead)
def get_distribution(distribution_id: int, db: Session = Depends(get_db)):
    """Obtém uma distribuição interna pelo ID."""
    distribution = db.query(InternalDistribution).filter(
        InternalDistribution.id == distribution_id
    ).first()
    if not distribution:
        raise HTTPException(status_code=404, detail="Distribuição não encontrada")
    return distribution


@router.post("", response_model=InternalDistributionRead, status_code=201)
def create_distribution(
    distribution: InternalDistributionCreate,
    db: Session = Depends(get_db)
):
    """
    Cria uma nova distribuição interna com registro automático de movimentação de estoque.
    
    COMENTÁRIO DE AUDITORIA: Esta rota implementa a lógica transacional completa:
    1. Valida se há estoque suficiente na loja de origem
    2. Cria o cabeçalho da distribuição (InternalDistribution)
    3. Cria todos os itens (InternalDistributionItem)
    4. Registra as movimentações de estoque (transfer_out e transfer_in) e atualiza StockStore
    
    Se qualquer erro ocorrer, a transação é revertida e nenhuma movimentação é registrada.
    """
    try:
        # Validar estoque na loja de origem
        items_list = [item.dict() for item in distribution.items]
        is_valid, error_msg = DistributionsService.validate_distribution_items_stock(
            db, distribution.from_store_id, items_list
        )
        
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # Criar distribuição
        db_distribution = InternalDistribution(
            from_store_id=distribution.from_store_id,
            to_store_id=distribution.to_store_id,
            distribution_date=distribution.distribution_date,
            status=distribution.status,
        )
        db.add(db_distribution)
        db.flush()

        # Criar itens
        for item_data in distribution.items:
            db_item = InternalDistributionItem(
                internal_distribution_id=db_distribution.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                registered_at=item_data.registered_at,
            )
            db.add(db_item)
        db.flush()

        # Registrar movimentações de estoque
        DistributionsService.register_transfer_movements(db, db_distribution.id)

        # Commit da transação
        db.commit()
        db.refresh(db_distribution)
        return db_distribution

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar distribuição: {str(e)}")


@router.put("/{distribution_id}", response_model=InternalDistributionRead)
def update_distribution(
    distribution_id: int,
    status: str = Query(..., description="Novo status da distribuição"),
    db: Session = Depends(get_db)
):
    """Atualiza o status de uma distribuição interna."""
    db_distribution = db.query(InternalDistribution).filter(
        InternalDistribution.id == distribution_id
    ).first()
    if not db_distribution:
        raise HTTPException(status_code=404, detail="Distribuição não encontrada")
    
    db_distribution.status = status
    db.commit()
    db.refresh(db_distribution)
    return db_distribution


@router.delete("/{distribution_id}", status_code=204)
def delete_distribution(distribution_id: int, db: Session = Depends(get_db)):
    """Deleta uma distribuição interna."""
    db_distribution = db.query(InternalDistribution).filter(
        InternalDistribution.id == distribution_id
    ).first()
    if not db_distribution:
        raise HTTPException(status_code=404, detail="Distribuição não encontrada")
    
    # Deletar itens associados
    db.query(InternalDistributionItem).filter(
        InternalDistributionItem.internal_distribution_id == distribution_id
    ).delete()
    
    db.delete(db_distribution)
    db.commit()
