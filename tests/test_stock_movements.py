"""
Testes para fluxos críticos de movimentação de estoque.

Estes testes validam:
1. Criação de entrada de produto com atualização automática de estoque
2. Criação de distribuição interna com validação de estoque
3. Criação de venda com validação de estoque insuficiente
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base, get_db
from app.models import (
    Client, Category, Product, Supplier, Store,
    StockStore, StockMovement
)

# Usar banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override da dependência get_db para usar banco de testes."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Setup do banco de dados para cada teste."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def create_test_data():
    """Cria dados de teste."""
    db = TestingSessionLocal()
    
    # Criar categoria
    category = Category(name="Eletrônicos", description="Produtos eletrônicos")
    db.add(category)
    db.flush()
    
    # Criar produto
    product = Product(
        name="Notebook",
        description="Notebook de 15 polegadas",
        cost_price=2000.0,
        sale_price=3000.0,
        active=True,
        category_id=category.id,
    )
    db.add(product)
    db.flush()
    
    # Criar segundo produto
    product2 = Product(
        name="Mouse",
        description="Mouse sem fio",
        cost_price=50.0,
        sale_price=100.0,
        active=True,
        category_id=category.id,
    )
    db.add(product2)
    db.flush()
    
    # Criar fornecedor
    supplier = Supplier(
        name="Tech Supplies",
        cnpj="12.345.678/0001-00",
        contact_info="contato@techsupplies.com",
    )
    db.add(supplier)
    db.flush()
    
    # Criar lojas
    store1 = Store(name="Loja Centro", address="Rua A, 100")
    store2 = Store(name="Loja Zona Leste", address="Rua B, 200")
    db.add(store1)
    db.add(store2)
    db.flush()
    
    # Criar cliente
    client_obj = Client(
        name="João Silva",
        cpf_cnpj="123.456.789-00",
        email="joao@example.com",
        phone="11999999999",
    )
    db.add(client_obj)
    db.flush()
    
    db.commit()
    
    return {
        "category": category,
        "product": product,
        "product2": product2,
        "supplier": supplier,
        "store1": store1,
        "store2": store2,
        "client": client_obj,
    }


def test_create_entry_with_stock_movement(create_test_data):
    """Testa criação de entrada de produto com movimentação automática de estoque."""
    data = create_test_data
    
    entry_data = {
        "supplier_id": data["supplier"].id,
        "entry_date": "2025-12-08T10:00:00Z",
        "invoice_number": "NF-001",
        "total_value": 2000.0,
        "status": "received",
        "items": [
            {
                "product_id": data["product"].id,
                "quantity": 10,
                "unit_price": 200.0,
                "total_price": 2000.0,
                "lot_number": "LOTE-001",
                "expiration_date": "2026-12-31T00:00:00Z",
                "received_at": "2025-12-08T10:00:00Z",
            }
        ],
    }
    
    response = client.post(
        f"/entries?store_id={data['store1'].id}",
        json=entry_data,
    )
    
    assert response.status_code == 201
    entry = response.json()
    assert entry["supplier_id"] == data["supplier"].id
    assert len(entry["items"]) == 1
    
    # Verificar se o estoque foi atualizado
    db = TestingSessionLocal()
    stock = db.query(StockStore).filter(
        StockStore.store_id == data["store1"].id,
        StockStore.product_id == data["product"].id,
    ).first()
    
    assert stock is not None
    assert stock.quantity == 10
    
    # Verificar se a movimentação foi registrada
    movement = db.query(StockMovement).filter(
        StockMovement.product_id == data["product"].id,
        StockMovement.store_id == data["store1"].id,
        StockMovement.movement_type == "entry",
    ).first()
    
    assert movement is not None
    assert movement.stock_before == 0
    assert movement.stock_after == 10
    assert movement.reference_type == "entry"
    
    db.close()


def test_create_sale_with_sufficient_stock(create_test_data):
    """Testa criação de venda com estoque suficiente."""
    data = create_test_data
    db = TestingSessionLocal()
    
    # Criar estoque inicial
    stock = StockStore(
        store_id=data["store1"].id,
        product_id=data["product"].id,
        quantity=20,
    )
    db.add(stock)
    db.commit()
    db.close()
    
    sale_data = {
        "client_id": data["client"].id,
        "store_id": data["store1"].id,
        "sale_date": "2025-12-08T14:00:00Z",
        "delivery_type": "express",
        "tracking_code": "TRK-001",
        "status": "completed",
        "predicted_delivery": "2025-12-09T18:00:00Z",
        "delivered_at": "2025-12-08T14:00:00Z",
        "total_value": 600.0,
        "items": [
            {
                "product_id": data["product"].id,
                "quantity": 2,
                "unit_price": 300.0,
                "total_price": 600.0,
                "removed_at": "2025-12-08T14:00:00Z",
            }
        ],
    }
    
    response = client.post("/sales", json=sale_data)
    
    assert response.status_code == 201
    sale = response.json()
    assert sale["client_id"] == data["client"].id
    assert len(sale["items"]) == 1
    
    # Verificar se o estoque foi decrementado
    db = TestingSessionLocal()
    stock = db.query(StockStore).filter(
        StockStore.store_id == data["store1"].id,
        StockStore.product_id == data["product"].id,
    ).first()
    
    assert stock.quantity == 18
    
    # Verificar se a movimentação foi registrada
    movement = db.query(StockMovement).filter(
        StockMovement.product_id == data["product"].id,
        StockMovement.store_id == data["store1"].id,
        StockMovement.movement_type == "sale",
    ).first()
    
    assert movement is not None
    assert movement.stock_before == 20
    assert movement.stock_after == 18
    assert movement.reference_type == "sale"
    
    db.close()


def test_create_sale_with_insufficient_stock(create_test_data):
    """Testa criação de venda com estoque insuficiente."""
    data = create_test_data
    db = TestingSessionLocal()
    
    # Criar estoque inicial pequeno
    stock = StockStore(
        store_id=data["store1"].id,
        product_id=data["product"].id,
        quantity=5,
    )
    db.add(stock)
    db.commit()
    db.close()
    
    sale_data = {
        "client_id": data["client"].id,
        "store_id": data["store1"].id,
        "sale_date": "2025-12-08T14:00:00Z",
        "delivery_type": "express",
        "tracking_code": "TRK-002",
        "status": "pending",
        "predicted_delivery": "2025-12-09T18:00:00Z",
        "delivered_at": None,
        "total_value": 6000.0,
        "items": [
            {
                "product_id": data["product"].id,
                "quantity": 10,  # Mais do que o disponível
                "unit_price": 600.0,
                "total_price": 6000.0,
                "removed_at": None,
            }
        ],
    }
    
    response = client.post("/sales", json=sale_data)
    
    assert response.status_code == 400
    assert "Estoque insuficiente" in response.json()["detail"]


def test_create_distribution_with_stock_movement(create_test_data):
    """Testa criação de distribuição interna com movimentação automática."""
    data = create_test_data
    db = TestingSessionLocal()
    
    # Criar estoque na loja de origem
    stock = StockStore(
        store_id=data["store1"].id,
        product_id=data["product"].id,
        quantity=30,
    )
    db.add(stock)
    db.commit()
    db.close()
    
    distribution_data = {
        "from_store_id": data["store1"].id,
        "to_store_id": data["store2"].id,
        "distribution_date": "2025-12-08T12:00:00Z",
        "status": "in_transit",
        "items": [
            {
                "product_id": data["product"].id,
                "quantity": 10,
                "registered_at": "2025-12-08T12:00:00Z",
            }
        ],
    }
    
    response = client.post("/internal-distributions", json=distribution_data)
    
    assert response.status_code == 201
    distribution = response.json()
    assert distribution["from_store_id"] == data["store1"].id
    assert distribution["to_store_id"] == data["store2"].id
    
    # Verificar estoque na loja de origem (decrementado)
    db = TestingSessionLocal()
    stock_origin = db.query(StockStore).filter(
        StockStore.store_id == data["store1"].id,
        StockStore.product_id == data["product"].id,
    ).first()
    assert stock_origin.quantity == 20
    
    # Verificar estoque na loja de destino (incrementado)
    stock_dest = db.query(StockStore).filter(
        StockStore.store_id == data["store2"].id,
        StockStore.product_id == data["product"].id,
    ).first()
    assert stock_dest.quantity == 10
    
    # Verificar movimentações
    movements = db.query(StockMovement).filter(
        StockMovement.reference_id == distribution["id"],
        StockMovement.reference_type == "distribution",
    ).all()
    
    assert len(movements) == 2  # transfer_out e transfer_in
    
    transfer_out = next(m for m in movements if m.movement_type == "transfer_out")
    transfer_in = next(m for m in movements if m.movement_type == "transfer_in")
    
    assert transfer_out.stock_before == 30
    assert transfer_out.stock_after == 20
    assert transfer_in.stock_before == 0
    assert transfer_in.stock_after == 10
    
    db.close()


def test_create_distribution_with_insufficient_stock(create_test_data):
    """Testa criação de distribuição com estoque insuficiente na origem."""
    data = create_test_data
    db = TestingSessionLocal()
    
    # Criar estoque pequeno na loja de origem
    stock = StockStore(
        store_id=data["store1"].id,
        product_id=data["product"].id,
        quantity=5,
    )
    db.add(stock)
    db.commit()
    db.close()
    
    distribution_data = {
        "from_store_id": data["store1"].id,
        "to_store_id": data["store2"].id,
        "distribution_date": "2025-12-08T12:00:00Z",
        "status": "pending",
        "items": [
            {
                "product_id": data["product"].id,
                "quantity": 10,  # Mais do que o disponível
                "registered_at": "2025-12-08T12:00:00Z",
            }
        ],
    }
    
    response = client.post("/internal-distributions", json=distribution_data)
    
    assert response.status_code == 400
    assert "Estoque insuficiente" in response.json()["detail"]
