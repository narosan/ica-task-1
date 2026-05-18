# Imagem slim — menor tamanho, sem dependências desnecessárias
FROM python:3.12-slim

# Boa prática: evita que o Python bufferize logs (você vê os prints em tempo real)
# Equivalente a rodar: python -u
ENV PYTHONUNBUFFERED=1

# Evita geração de .pyc desnecessários dentro do container
ENV PYTHONDONTWRITEBYTECODE=1

ENV FLASK_APP=main.py    

WORKDIR /app

COPY requirements.txt .          
RUN pip install --no-cache-dir -r requirements.txt 

# Copia o projeto
COPY . .

# Cria o diretório data com permissão de escrita
# (seu repositório salva os .txt aqui)
RUN mkdir -p /app/data

# Instala apenas o Flask — sem requirements.txt, declaramos direto
RUN pip install --no-cache-dir flask

# Expõe a porta padrão do Flask
EXPOSE 5000

# Roda a aplicação
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]