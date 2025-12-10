"""
Serviço de gerenciamento de estoque.

Este módulo implementa a lógica de movimentação de estoque com atomicidade garantida.
Todas as operações que afetam o estoque (entrada, distribuição, venda) devem passar
por este serviço para garantir a integridade dos dados.
"""
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import StockStore, StockMovement, Product, Store


class StockService:
    """Serviço para gerenciar movimentações de estoque."""

    @staticmethod
    def get_or_create_stock(
        db: Session,
        store_id: int,
        product_id: int,
    ) -> StockStore:
        """
        Obtém ou cria um registro de estoque para uma loja e produto.
        
        Args:
            db: Sessão do banco de dados
            store_id: ID da loja
            product_id: ID do produto
            
        Returns:
            StockStore: Registro de estoque
        """
        stock = db.query(StockStore).filter(
            StockStore.store_id == store_id,
            StockStore.product_id == product_id,
        ).first()

        if not stock:
            stock = StockStore(
                store_id=store_id,
                product_id=product_id,
                quantity=0,
                updated_at=datetime.utcnow(),
            )
            db.add(stock)
            db.flush()

        return stock

    @staticmethod
    def register_movement(
        db: Session,
        product_id: int,
        store_id: int,
        movement_type: str,
        quantity: int,
        reference_id: int | None = None,
        reference_type: str | None = None,
        notes: str | None = None,
    ) -> StockMovement:
        """
        Registra uma movimentação de estoque com atualização automática do StockStore.
        
        COMENTÁRIO DE AUDITORIA: Esta função é o ponto central para qualquer movimentação
        de estoque. Ela garante que:
        1. O estoque atual (stock_before) é capturado antes da alteração
        2. O estoque é atualizado de acordo com o tipo de movimento
        3. O novo estoque (stock_after) é registrado
        4. Um registro de auditoria (StockMovement) é criado com todas as informações
        
        Tipos de movimento suportados:
        - 'entry': entrada de produto (incrementa estoque)
        - 'sale': venda (decrementa estoque)
        - 'transfer_out': saída por transferência interna (decrementa estoque)
        - 'transfer_in': entrada por transferência interna (incrementa estoque)
        - 'adjustment_in': ajuste positivo (incrementa estoque)
        - 'adjustment_out': ajuste negativo (decrementa estoque)
        
        Args:
            db: Sessão do banco de dados
            product_id: ID do produto
            store_id: ID da loja
            movement_type: Tipo de movimento
            quantity: Quantidade movimentada
            reference_id: ID da referência (entrada, venda, distribuição, etc.)
            reference_type: Tipo de referência ('entry', 'sale', 'distribution', 'adjustment')
            notes: Notas adicionais
            
        Returns:
            StockMovement: Registro de movimentação criado
            
        Raises:
            ValueError: Se o tipo de movimento for inválido
        """
        # Validar tipo de movimento
        valid_types = {'entry', 'sale', 'transfer_out', 'transfer_in', 'adjustment_in', 'adjustment_out'}
        if movement_type not in valid_types:
            raise ValueError(f"Tipo de movimento inválido: {movement_type}")

        # Obter ou criar registro de estoque
        stock = StockService.get_or_create_stock(db, store_id, product_id)
        stock_before = stock.quantity

        # Calcular novo estoque com base no tipo de movimento
        if movement_type in ['entry', 'transfer_in', 'adjustment_in']:
            stock_after = stock_before + quantity
        elif movement_type in ['sale', 'transfer_out', 'adjustment_out']:
            stock_after = stock_before - quantity
        else:
            stock_after = stock_before

        # Atualizar estoque
        stock.quantity = stock_after
        stock.updated_at = datetime.utcnow()

        # Criar registro de movimentação (auditoria)
        movement = StockMovement(
            product_id=product_id,
            store_id=store_id,
            movement_type=movement_type,
            quantity=quantity,
            movement_date=datetime.utcnow(),
            reference_id=reference_id,
            reference_type=reference_type,
            stock_before=stock_before,
            stock_after=stock_after,
            notes=notes,
        )
        db.add(movement)
        db.flush()

        return movement

    @staticmethod
    def validate_stock_availability(
        db: Session,
        store_id: int,
        product_id: int,
        required_quantity: int,
    ) -> bool:
        """
        Valida se há estoque suficiente para uma operação.
        
        Args:
            db: Sessão do banco de dados
            store_id: ID da loja
            product_id: ID do produto
            required_quantity: Quantidade necessária
            
        Returns:
            bool: True se há estoque suficiente, False caso contrário
        """
        stock = db.query(StockStore).filter(
            StockStore.store_id == store_id,
            StockStore.product_id == product_id,
        ).first()

        if not stock:
            return False

        return stock.quantity >= required_quantity

    @staticmethod
    def get_stock_by_store_and_product(
        db: Session,
        store_id: int,
        product_id: int,
    ) -> int:
        """
        Obtém a quantidade de estoque para uma loja e produto.
        
        Args:
            db: Sessão do banco de dados
            store_id: ID da loja
            product_id: ID do produto
            
        Returns:
            int: Quantidade de estoque (0 se não existir)
        """
        stock = db.query(StockStore).filter(
            StockStore.store_id == store_id,
            StockStore.product_id == product_id,
        ).first()

        return stock.quantity if stock else 0
