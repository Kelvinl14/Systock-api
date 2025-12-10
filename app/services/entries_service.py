"""
Serviço de gerenciamento de entradas de produtos.

Este módulo implementa a lógica de criação de entradas de produtos com
registro automático de movimentações de estoque.
"""
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import ProductEntry, ProductEntryItem
from app.services.stock_service import StockService


class EntriesService:
    """Serviço para gerenciar entradas de produtos."""

    @staticmethod
    def register_entry_movements(
        db: Session,
        product_entry_id: int,
        store_id: int = 1,
    ) -> list:
        """
        Registra as movimentações de estoque para uma entrada de produtos.
        
        COMENTÁRIO DE AUDITORIA: Esta função é chamada após a criação de uma
        ProductEntry e seus ProductEntryItems. Para cada item, ela:
        1. Incrementa o estoque na loja (StockStore.quantity += item.quantity)
        2. Cria um registro de auditoria em StockMovement com:
           - movement_type='entry'
           - reference_type='entry'
           - reference_id=product_entry_id
           - stock_before e stock_after capturados no mesmo escopo de transação
        
        Args:
            db: Sessão do banco de dados
            product_entry_id: ID da entrada de produtos
            store_id: ID da loja (padrão: 1)
            
        Returns:
            list: Lista de movimentações criadas
        """
        # Buscar itens da entrada
        items = db.query(ProductEntryItem).filter(
            ProductEntryItem.product_entry_id == product_entry_id
        ).all()

        movements = []
        for item in items:
            # Registrar movimentação de entrada
            movement = StockService.register_movement(
                db=db,
                product_id=item.product_id,
                store_id=store_id,
                movement_type='entry',
                quantity=item.quantity,
                reference_id=product_entry_id,
                reference_type='entry',
                notes=f"Entrada de produto - Fornecedor: {item.product_entry_id}",
            )
            movements.append(movement)

        return movements
