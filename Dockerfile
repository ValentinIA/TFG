FROM python:3.10

WORKDIR /app


# Copiar y instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Luego ejecuta la instalación de los navegadores
RUN playwright instsdfsdfsdall chromium

# Copiar el código de la app
COPY . .

EXPOSE 8000

CMD ["uvicorn", "Rutas:app", "--host", "0.0.0.0", "--port", "8000"]
