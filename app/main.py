"""
Aplicação principal FastAPI para Systock.

Esta aplicação implementa uma API completa para gerenciamento de estoque multi-loja
com controle de entradas, distribuições internas, vendas e rastreamento automático
de movimentações.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import Base, engine
from app.routers import (
    clients,
    categories,
    products,
    suppliers,
    stores,
    carriers,
    stock,
    movements,
    entries,
    internal_distributions,
    sales,
)

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="API de gerenciamento de estoque multi-loja com rastreamento automático de movimentações",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(clients.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(suppliers.router)
app.include_router(stores.router)
app.include_router(carriers.router)
app.include_router(stock.router)
app.include_router(movements.router)
app.include_router(entries.router)
app.include_router(internal_distributions.router)
app.include_router(sales.router)


@app.get("/", tags=["health"])
def read_root():
    """Health check da API."""
    return {
        "message": "Systock API",
        "version": settings.api_version,
        "status": "running",
    }


@app.get("/health", tags=["health"])
def health_check():
    """Health check detalhado."""
    return {
        "status": "healthy",
        "api_title": settings.api_title,
        "api_version": settings.api_version,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
