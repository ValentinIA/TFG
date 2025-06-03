FROM python:3.10

WORKDIR /app

# Copiar y instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instala las dependencias necesarias para Chromium
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    wget \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Instalar playwright (si no está en requirements.txt)
RUN pip install playwright

# Instala navegador Chromium
RUN playwright install chromium

# Copiar el código de la app
COPY . .

EXPOSE 8000

# Ejecutar la aplicación
CMD ["uvicorn", "Rutas:app", "--host", "0.0.0.0", "--port", "8000"]
