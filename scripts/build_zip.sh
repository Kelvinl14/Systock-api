#!/bin/bash

# Script para empacotar o projeto Systock API em um arquivo ZIP

set -e

PROJECT_NAME="systock-api"
VERSION="1.0.0"
OUTPUT_DIR="./dist"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ZIP_NAME="${PROJECT_NAME}-${VERSION}-${TIMESTAMP}.zip"

echo "=========================================="
echo "Systock API - Build ZIP Script"
echo "=========================================="
echo ""

# Criar diretório de saída
mkdir -p "$OUTPUT_DIR"

# Limpar arquivos de cache
echo "Limpando arquivos de cache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
find . -type d -name .egg-info -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Criar arquivo ZIP
echo "Criando arquivo ZIP: $ZIP_NAME"
zip -r "$OUTPUT_DIR/$ZIP_NAME" \
    app/ \
    tests/ \
    alembic/ \
    scripts/ \
    requirements.txt \
    .env.example \
    Dockerfile \
    docker-compose.yml \
    README.md \
    -x "*.pyc" \
    "__pycache__/*" \
    ".pytest_cache/*" \
    ".git/*" \
    ".gitignore" \
    "*.egg-info/*" \
    "dist/*" \
    ".env" \
    ".venv/*" \
    "venv/*"

echo ""
echo "=========================================="
echo "✓ Arquivo ZIP criado com sucesso!"
echo "=========================================="
echo ""
echo "Localização: $OUTPUT_DIR/$ZIP_NAME"
echo "Tamanho: $(du -h "$OUTPUT_DIR/$ZIP_NAME" | cut -f1)"
echo ""
echo "Para descompactar:"
echo "  unzip $OUTPUT_DIR/$ZIP_NAME"
echo ""
echo "Para rodar com Docker:"
echo "  docker-compose up -d"
echo ""
echo "Para rodar localmente:"
echo "  pip install -r requirements.txt"
echo "  uvicorn app.main:app --reload"
echo ""
