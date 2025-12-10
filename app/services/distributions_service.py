"""
Serviço de gerenciamento de distribuições internas.

Este módulo implementa a lógica de criação de distribuições internas entre lojas
com registro automático de movimentações de estoque.
"""
from sqlalchemy.orm import Session
from app.models import InternalDistribution, InternalDistributionItem
from app.services.stock_service import StockService


class DistributionsService:
    """Serviço para gerenciar distribuições internas."""

    @staticmethod
    def validate_distribution_items_stock(
        db: Session,
        from_store_id: int,
        items: list[dict],
    ) -> tuple[bool, str]:
        """
        Valida se há estoque suficiente na loja de origem para todos os itens.
        
        Args:
            db: Sessão do banco de dados
            from_store_id: ID da loja de origem
            items: Lista de itens com 'product_id' e 'quantity'
            
        Returns:
            tuple: (bool, str) - (sucesso, mensagem de erro se houver)
        """
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity')

            if not StockService.validate_stock_availability(
                db, from_store_id, product_id, quantity
            ):
                current_stock = StockService.get_stock_by_store_and_product(
                    db, from_store_id, product_id
                )
                return False, (
                    f"Estoque insuficiente na loja de origem para o produto {product_id}. "
                    f"Disponível: {current_stock}, Solicitado: {quantity}"
                )

        return True, ""

    @staticmethod
    def register_transfer_movements(
        db: Session,
        distribution_id: int,
    ) -> list:
        """
        Registra as movimentações de estoque para uma distribuição interna.
        
        COMENTÁRIO DE AUDITORIA: Esta função é chamada após a criação de uma
        InternalDistribution e seus InternalDistributionItems. Para cada item, ela:
        1. Decrementa o estoque na loja de origem (transfer_out)
        2. Incrementa o estoque na loja de destino (transfer_in)
        3. Cria dois registros de auditoria em StockMovement:
           - Um com movement_type='transfer_out' na loja de origem
           - Um com movement_type='transfer_in' na loja de destino
           - Ambos com reference_type='distribution' e reference_id=distribution_id
        
        Esta abordagem de dois registros facilita a auditoria e o rastreamento
        do estoque em cada loja individualmente.
        
        Args:
            db: Sessão do banco de dados
            distribution_id: ID da distribuição interna
            
        Returns:
            list: Lista de movimentações criadas
        """
        # Buscar distribuição
        distribution = db.query(InternalDistribution).filter(
            InternalDistribution.id == distribution_id
        ).first()

        if not distribution:
            return []

        # Buscar itens da distribuição
        items = db.query(InternalDistributionItem).filter(
            InternalDistributionItem.internal_distribution_id == distribution_id
        ).all()

        movements = []
        for item in items:
            # Registrar saída na loja de origem
            out_movement = StockService.register_movement(
                db=db,
                product_id=item.product_id,
                store_id=distribution.from_store_id,
                movement_type='transfer_out',
                quantity=item.quantity,
                reference_id=distribution_id,
                reference_type='distribution',
                notes=f"Transferência para loja {distribution.to_store_id}",
            )
            movements.append(out_movement)

            # Registrar entrada na loja de destino
            in_movement = StockService.register_movement(
                db=db,
                product_id=item.product_id,
                store_id=distribution.to_store_id,
                movement_type='transfer_in',
                quantity=item.quantity,
                reference_id=distribution_id,
                reference_type='distribution',
                notes=f"Transferência da loja {distribution.from_store_id}",
            )
            movements.append(in_movement)

        return movements
