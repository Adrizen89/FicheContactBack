# Stage 1: Builder
FROM python:3.12-slim as builder

WORKDIR /app

# Installation des dépendances système nécessaires pour psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

# Installation de libpq pour psycopg2
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copier les dépendances depuis le builder
COPY --from=builder /root/.local /root/.local

# Copier le code de l'application
COPY . .

# Ajouter les scripts Python au PATH
ENV PATH=/root/.local/bin:$PATH

# Exposer le port de l'API
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/')" || exit 1

# Commande de démarrage
CMD ["uvicorn", "infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
