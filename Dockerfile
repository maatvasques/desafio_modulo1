# Usa a imagem oficial do Odoo 17 como base
FROM odoo:17.0

# Copia o arquivo requirements.txt para o contêiner
COPY ./requirements.txt /tmp/requirements.txt

# Instala as dependências Python
RUN pip3 install -r /tmp/requirements.txt