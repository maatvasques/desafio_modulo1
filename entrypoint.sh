#!/bin/bash
# entrypoint.sh

echo "Aguardando o banco de dados..."
until PGPASSWORD=$PASSWORD pg_isready -h $HOST -U $USER -p 5432; do
  echo "mydb:5432 - ainda indisponível. Aguardando..."
  sleep 1
done
echo "Postgres está disponível - iniciando Odoo"

# Instala o debugpy para debug
pip install --user debugpy

# Inicia o Odoo com debugpy usando o arquivo de configuração
/usr/bin/python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client /usr/bin/odoo -c /etc/odoo/odoo.conf