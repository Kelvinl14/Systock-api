"""
Serviço de gerenciamento de vendas.

Este módulo implementa a lógica de criação de vendas com validação de estoque
e registro automático de movimentações de estoque.
"""
from sqlalchemy.orm import Session
from app.models import Sale, SaleItem
from app.services.stock_service import StockService


class SalesService:
    """Serviço para gerenciar vendas."""

    @staticmethod
    def validate_sale_items_stock(
        db: Session,
        store_id: int,
        items: list[dict],
    ) -> tuple[bool, str]:
        """
        Valida se há estoque suficiente para todos os itens de uma venda.
        
        Args:
            db: Sessão do banco de dados
            store_id: ID da loja
            items: Lista de itens com 'product_id' e 'quantity'
            
        Returns:
            tuple: (bool, str) - (sucesso, mensagem de erro se houver)
        """
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity')

            if not StockService.validate_stock_availability(
                db, store_id, product_id, quantity
            ):
                current_stock = StockService.get_stock_by_store_and_product(
                    db, store_id, product_id
                )
                return False, (
                    f"Estoque insuficiente para o produto {product_id}. "
                    f"Disponível: {current_stock}, Solicitado: {quantity}"
                )

        return True, ""

    @staticmethod
    def register_sale_movements(
        db: Session,
        sale_id: int,
    ) -> list:
        """
        Registra as movimentações de estoque para uma venda.
        
        COMENTÁRIO DE AUDITORIA: Esta função é chamada após a criação de uma
        Sale e seus SaleItems. Para cada item, ela:
        1. Decrementa o estoque na loja (StockStore.quantity -= item.quantity)
        2. Cria um registro de auditoria em StockMovement com:
           - movement_type='sale'
           - reference_type='sale'
           - reference_id=sale_id
           - stock_before e stock_after capturados no mesmo escopo de transação
        
        Args:
            db: Sessão do banco de dados
            sale_id: ID da venda
            
        Returns:
            list: Lista de movimentações criadas
        """
        # Buscar venda para obter store_id
        sale = db.query(Sale).filter(Sale.id == sale_id).first()
        if not sale:
            return []

        # Buscar itens da venda
        items = db.query(SaleItem).filter(SaleItem.sale_id == sale_id).all()

        movements = []
        for item in items:
            # Registrar movimentação de venda
            movement = StockService.register_movement(
                db=db,
                product_id=item.product_id,
                store_id=sale.store_id,
                movement_type='sale',
                quantity=item.quantity,
                reference_id=sale_id,
                reference_type='sale',
                notes=f"Venda #{sale_id} - Cliente: {sale.client_id}",
            )
            movements.append(movement)

        return movements
