FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip

# Timeout augmenté à 3600 secondes (1 heure) pour PyTorch
RUN pip install --no-cache-dir --default-timeout=3600 -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]