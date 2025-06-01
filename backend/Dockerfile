# Etapa 1: builder
FROM python:3.12-slim AS builder

# Evitar prompts de tzdata, etc.
ENV DEBIAN_FRONTEND=noninteractive

# Instalar libpq (Postgres) y wkhtmltopdf dependencias de pdfkit
RUN apt-get update && apt-get install -y \
    build-essential wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia sólo archivos de dependencias para cache más eficiente
COPY backend/requirements.txt .

RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# Etapa 2: runtime (imagen final más liviana)
FROM python:3.12-slim

WORKDIR /app

# Copia lo instalado desde la etapa builder
COPY --from=builder /install /usr/local
# Copia el código fuente
COPY backend/ ./

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]