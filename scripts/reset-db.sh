#!/bin/bash

echo "🚀 Resetando banco de dados 'systock' no container systock_db..."

# Verifica se o container está ativo
if ! docker ps --format '{{.Names}}' | grep -q "systock_db"; then
  echo "❌ ERRO: O container systock_db não está em execução."
  exit 1
fi

# Executa o TRUNCATE em todas as tabelas automaticamente
docker exec -i systock_db psql -U postgres -d systock <<'EOF'
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' RESTART IDENTITY CASCADE;';
    END LOOP;
END $$;
EOF

echo "✅ Banco de dados resetado com sucesso!"
