# Systock API - Gerenciamento de Estoque Multi-Loja

Uma API FastAPI completa para gerenciamento de estoque com suporte a múltiplas lojas, controle de entradas de produtos, distribuições internas e vendas, com rastreamento automático de movimentações.

## 📋 Características

- **CRUD Completo** para todas as entidades (clientes, categorias, produtos, fornecedores, lojas, transportadoras)
- **Gestão de Estoque** com rastreamento por loja e produto
- **Entradas de Produtos** com registro automático de movimentações
- **Distribuições Internas** entre lojas com validação de estoque
- **Vendas** com validação de estoque insuficiente
- **Auditoria Completa** de movimentações de estoque (stock_before, stock_after)
- **Transações Atômicas** para garantir integridade dos dados
- **Documentação Automática** via Swagger/OpenAPI
- **Testes Automatizados** com pytest
- **Docker & Docker Compose** para fácil deployment

## 🚀 Quick Start

### Pré-requisitos

- Python 3.11+
- pip ou poetry
- Docker e Docker Compose (opcional)

### Instalação Local

```bash
# Clonar repositório
git clone [<repo-url>](https://github.com/Kelvinl14/Systock-api?tab=readme-ov-file)
cd systock-api

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações de banco de dados

# Rodar migrations (se usar Alembic)
# alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

Documentação Swagger: `http://localhost:8000/docs`

### Instalação com Docker

```bash
# Construir e rodar containers
docker-compose up -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f api
```

A API estará disponível em: `http://localhost:8000`

## 📚 Estrutura do Projeto

```
systock-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicação principal FastAPI
│   ├── core/
│   │   ├── config.py          # Configurações
│   │   └── __init__.py
│   ├── db/
│   │   ├── database.py        # Configuração do banco de dados
│   │   └── __init__.py
│   ├── models/                # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── supplier.py
│   │   ├── store.py
│   │   ├── stock_store.py
│   │   ├── product_entry.py
│   │   ├── internal_distribution.py
│   │   ├── carrier.py
│   │   ├── sale.py
│   │   └── stock_movement.py
│   ├── schemas/               # Schemas Pydantic
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── supplier.py
│   │   ├── store.py
│   │   ├── stock_store.py
│   │   ├── product_entry.py
│   │   ├── internal_distribution.py
│   │   ├── carrier.py
│   │   ├── sale.py
│   │   └── stock_movement.py
│   ├── routers/               # Routers FastAPI
│   │   ├── __init__.py
│   │   ├── clients.py
│   │   ├── categories.py
│   │   ├── products.py
│   │   ├── suppliers.py
│   │   ├── stores.py
│   │   ├── carriers.py
│   │   ├── stock.py
│   │   ├── movements.py
│   │   ├── entries.py
│   │   ├── internal_distributions.py
│   │   └── sales.py
│   ├── services/              # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── stock_service.py
│   │   ├── entries_service.py
│   │   ├── sales_service.py
│   │   └── distributions_service.py
│   └── utils/
├── tests/                     # Testes automatizados
│   ├── __init__.py
│   └── test_stock_movements.py
├── alembic/                   # Migrations (Alembic)
│   └── versions/
├── scripts/
│   └── build_zip.sh          # Script de empacotamento
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🔌 Endpoints da API

### Clientes (`/clients`)
- `GET /clients` - Listar clientes com filtros
- `GET /clients/{id}` - Obter cliente por ID
- `POST /clients` - Criar novo cliente
- `PUT /clients/{id}` - Atualizar cliente
- `DELETE /clients/{id}` - Deletar cliente

### Categorias (`/categories`)
- `GET /categories` - Listar categorias
- `GET /categories/{id}` - Obter categoria por ID
- `POST /categories` - Criar categoria
- `PUT /categories/{id}` - Atualizar categoria
- `DELETE /categories/{id}` - Deletar categoria

### Produtos (`/products`)
- `GET /products` - Listar produtos com filtros (categoria, ativo)
- `GET /products/{id}` - Obter produto por ID
- `POST /products` - Criar produto
- `PUT /products/{id}` - Atualizar produto
- `DELETE /products/{id}` - Deletar produto

### Fornecedores (`/suppliers`)
- `GET /suppliers` - Listar fornecedores
- `GET /suppliers/{id}` - Obter fornecedor por ID
- `POST /suppliers` - Criar fornecedor
- `PUT /suppliers/{id}` - Atualizar fornecedor
- `DELETE /suppliers/{id}` - Deletar fornecedor

### Lojas (`/stores`)
- `GET /stores` - Listar lojas
- `GET /stores/{id}` - Obter loja por ID
- `POST /stores` - Criar loja
- `PUT /stores/{id}` - Atualizar loja
- `DELETE /stores/{id}` - Deletar loja

### Transportadoras (`/carriers`)
- `GET /carriers` - Listar transportadoras
- `GET /carriers/{id}` - Obter transportadora por ID
- `POST /carriers` - Criar transportadora
- `PUT /carriers/{id}` - Atualizar transportadora
- `DELETE /carriers/{id}` - Deletar transportadora

### Estoque (`/stock`)
- `GET /stock` - Listar estoque com filtros
- `GET /stock/{id}` - Obter estoque por ID
- `GET /stock/stores/{store_id}/products/{product_id}` - Obter quantidade de estoque
- `PUT /stock/{id}` - Atualizar estoque
- `DELETE /stock/{id}` - Deletar estoque

### Movimentações (`/movements`)
- `GET /movements` - Listar movimentações com filtros
- `GET /movements/{id}` - Obter movimentação por ID
- `GET /movements/by-reference/{reference_type}/{reference_id}` - Obter movimentações por referência

### Entradas de Produtos (`/entries`)
- `GET /entries` - Listar entradas
- `GET /entries/{id}` - Obter entrada por ID
- `POST /entries` - Criar entrada (com movimentação automática)
- `PUT /entries/{id}` - Atualizar status da entrada
- `DELETE /entries/{id}` - Deletar entrada

### Distribuições Internas (`/internal-distributions`)
- `GET /internal-distributions` - Listar distribuições
- `GET /internal-distributions/{id}` - Obter distribuição por ID
- `POST /internal-distributions` - Criar distribuição (com movimentação automática)
- `PUT /internal-distributions/{id}` - Atualizar status da distribuição
- `DELETE /internal-distributions/{id}` - Deletar distribuição

### Vendas (`/sales`)
- `GET /sales` - Listar vendas
- `GET /sales/{id}` - Obter venda por ID
- `POST /sales` - Criar venda (com validação de estoque)
- `PUT /sales/{id}` - Atualizar status da venda
- `DELETE /sales/{id}` - Deletar venda

## 📝 Exemplos de Requisições

### Criar Entrada de Produto

```bash
curl -X POST "http://localhost:8000/entries?store_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "supplier_id": 1,
    "entry_date": "2025-12-08T10:00:00Z",
    "invoice_number": "NF-20251208-001",
    "total_value": 1500.00,
    "status": "received",
    "items": [
      {
        "product_id": 1,
        "quantity": 50,
        "unit_price": 30.00,
        "total_price": 1500.00,
        "lot_number": "LOTE-A-2025",
        "expiration_date": "2026-12-31T00:00:00Z",
        "received_at": "2025-12-08T10:00:00Z"
      }
    ]
  }'
```

### Criar Distribuição Interna

```bash
curl -X POST "http://localhost:8000/internal-distributions" \
  -H "Content-Type: application/json" \
  -d '{
    "from_store_id": 1,
    "to_store_id": 2,
    "distribution_date": "2025-12-08T11:30:00Z",
    "status": "in_transit",
    "items": [
      {
        "product_id": 1,
        "quantity": 10,
        "registered_at": "2025-12-08T11:30:00Z"
      }
    ]
  }'
```

### Criar Venda

```bash
curl -X POST "http://localhost:8000/sales" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": 1,
    "store_id": 1,
    "sale_date": "2025-12-08T14:45:00Z",
    "delivery_type": "express",
    "tracking_code": "TRK-EXP-98765",
    "status": "completed",
    "predicted_delivery": "2025-12-09T18:00:00Z",
    "delivered_at": "2025-12-08T14:45:00Z",
    "total_value": 120.50,
    "items": [
      {
        "product_id": 1,
        "quantity": 2,
        "unit_price": 50.00,
        "total_price": 100.00,
        "removed_at": "2025-12-08T14:45:00Z"
      }
    ]
  }'
```

## 🧪 Testes

Executar testes automatizados:

```bash
# Instalar pytest
pip install pytest pytest-asyncio

# Rodar todos os testes
pytest

# Rodar com cobertura
pytest --cov=app tests/

# Rodar testes específicos
pytest tests/test_stock_movements.py -v
```

## 🔐 Variáveis de Ambiente

Criar arquivo `.env` baseado em `.env.example`:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/systock

# API Configuration
API_TITLE=Systock API
API_VERSION=1.0.0
DEBUG=True

# Logging
LOG_LEVEL=INFO
```

## 📦 Empacotamento

Criar arquivo ZIP com o projeto completo:

```bash
./scripts/build_zip.sh
```

O arquivo ZIP será criado em `dist/systock-api-1.0.0-TIMESTAMP.zip`

## 🗄️ Banco de Dados

### Modelos de Dados

A API implementa os seguintes modelos:

- **clients**: Clientes
- **categories**: Categorias de produtos
- **products**: Produtos
- **suppliers**: Fornecedores
- **stores**: Lojas
- **stock_store**: Estoque por loja e produto
- **product_entries**: Entradas de produtos
- **product_entry_items**: Itens de entradas
- **internal_distributions**: Distribuições internas
- **internal_distribution_items**: Itens de distribuições
- **carriers**: Transportadoras
- **sales**: Vendas
- **sale_items**: Itens de vendas
- **stock_movements**: Movimentações de estoque (auditoria)

### Criar Tabelas

As tabelas são criadas automaticamente ao iniciar a aplicação. Para usar Alembic:

```bash
# Gerar migration
alembic revision --autogenerate -m "Initial migration"

# Aplicar migration
alembic upgrade head
```

## 🔄 Fluxo de Movimentação de Estoque

### Entrada de Produto
1. Criar `ProductEntry` com `ProductEntryItem`s
2. Sistema registra automaticamente `StockMovement` com `movement_type='entry'`
3. `StockStore` é incrementado com a quantidade recebida

### Distribuição Interna
1. Validar estoque na loja de origem
2. Criar `InternalDistribution` com `InternalDistributionItem`s
3. Sistema registra dois `StockMovement`s:
   - `transfer_out` na loja de origem (decremento)
   - `transfer_in` na loja de destino (incremento)
4. `StockStore` é atualizado em ambas as lojas

### Venda
1. Validar estoque na loja
2. Se estoque insuficiente, retornar erro 400
3. Criar `Sale` com `SaleItem`s
4. Sistema registra `StockMovement` com `movement_type='sale'`
5. `StockStore` é decrementado com a quantidade vendida

## 📊 Auditoria

Todas as movimentações de estoque são registradas em `stock_movements` com:
- `stock_before`: Quantidade antes da movimentação
- `stock_after`: Quantidade após a movimentação
- `movement_type`: Tipo de movimento (entry, sale, transfer_out, transfer_in, adjustment_in, adjustment_out)
- `reference_id`: ID da referência (entrada, venda, distribuição)
- `reference_type`: Tipo de referência (entry, sale, distribution, adjustment)
- `movement_date`: Data/hora da movimentação
- `notes`: Notas adicionais

## 🐛 Troubleshooting

### Erro de conexão com banco de dados
Verificar se o banco está rodando e se `DATABASE_URL` está correto.

### Erro 404 em endpoints
Verificar se a rota está correta e se o recurso existe.

### Erro 400 em criação de entrada/distribuição/venda
Verificar mensagem de erro retornada. Geralmente relacionada a:
- Estoque insuficiente
- Dados inválidos
- Referência não encontrada

## 📞 Suporte

Para dúvidas ou issues, abrir uma issue no repositório.

## 📄 Licença

MIT License - veja LICENSE para detalhes.

---

**Versão**: 1.0.0  
**Última atualização**: 2025-12-10
