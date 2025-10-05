FROM python:3.13.1

# Definindo o local padrão para os arquivos dentro do docker
WORKDIR /app

# Instalando todas as libs necessarias
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiando todos os arquivos para o local padrão
COPY . .

# Expondo a porta 3000
EXPOSE 5000

# Executando o codigo
CMD ["python", "app.py"]