# ---------- Etapa builder ----------
FROM python:3.12-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

# ---------- Etapa runtime ----------
FROM python:3.12-slim
WORKDIR /app

# Instalar SOLO wkhtmltopdf y sus deps (no compila nada)
RUN apt-get update && apt-get install -y wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
#COPY backend/ ./
COPY . ./

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]