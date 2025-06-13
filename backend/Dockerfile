# --- STAGE 1: Builder ---
# Instala las dependencias en un directorio separado para mantener la imagen final ligera
FROM python:3.9-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt


# --- STAGE 2: Runner ---
# La imagen final que correrá la aplicación
FROM python:3.9-slim

# 👇 CORRECCIÓN: Instalar wkhtmltopdf y sus dependencias de fuentes
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wkhtmltopdf \
    xfonts-75dpi \
    xfonts-base \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .

EXPOSE 8000

