#!/bin/bash
# entrypoint.sh

echo "Aguardando o banco de dados..."
until PGPASSWORD=$PASSWORD pg_isready -h $HOST -U $USER -p 5432; do
  echo "mydb:5432 - ainda indisponível. Aguardando..."
  sleep 1
done
echo "Postgres está disponível - iniciando Odoo"

# Inicia o Odoo diretamente, sem o debugpy
/usr/bin/odoo -c /etc/odoo/odoo.conf