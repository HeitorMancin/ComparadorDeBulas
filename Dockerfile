# Escolher uma imagem base
FROM python:3.12

# Instale os pacotes de sistema necessários
RUN apt-get update && \
    apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 \
    libpangocairo-1.0-0 libcairo2 libgdk-pixbuf2.0-0 libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o contêiner
COPY . /app

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Definir o comando padrão a ser executado
CMD ["streamlit", "run", "Comparador.py", "--server.port", "8000", "--server.address", "0.0.0.0"]



