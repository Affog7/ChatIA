# Stage 1: Build (développement et installation des dépendances)
FROM python:3.12-slim AS builder

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

COPY requirement.txt .

# Installer les dépendances système (pour MySQL, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime (image finale légère pour production)
FROM python:3.12-slim AS production

# Installer les runtime deps minimales
RUN apt-get update && apt-get install -y \
    default-libmysqlclient21 \
    && rm -rf /var/lib/apt/lists/*

# Copier les dépendances installées du stage builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Définir le répertoire de travail
WORKDIR /app

# Copier le code source
COPY src/ ./src/

# Copier requirements.txt si besoin pour pip list (optionnel)
COPY requirements.txt .

# Exposer le port si c'est une app web (ex. : 8000 pour FastAPI/Uvicorn)
# EXPOSE 8000  # Décommentez si applicable

# Commande par défaut : lancer l'app (adaptez selon votre runner)
CMD ["python", "src/app.py"]

# Pour un déploiement web (ex. : avec Gunicorn si vous ajoutez FastAPI)
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "src.app:app"]  # Si app est une FastAPI instance