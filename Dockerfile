# Stage 1: Instalar dependências
FROM python:3.11-slim as builder

WORKDIR /usr/src/app

# Prevenir que o Python escreva arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Garantir que o output do Python não fique em buffer
ENV PYTHONUNBUFFERED 1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# Stage 2: Construir a imagem final
FROM python:3.11-slim

WORKDIR /home/user/app

# Criar um usuário não-root para rodar a aplicação por segurança
RUN addgroup --system app && adduser --system --group app

# Copiar dependências pré-compiladas do stage builder
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copiar o código da aplicação
COPY ./app .

# Mudar o proprietário dos arquivos para o usuário não-root
RUN chown -R app:app /home/user/app

# Mudar para o usuário não-root
USER app

# Expor a porta que o Gunicorn irá rodar
EXPOSE 5000

# Comando para rodar a aplicação em produção
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]