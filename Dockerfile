# Usa una imagen oficial de Python
FROM python:3.11

# Fija el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia solo el archivo de dependencias primero (para aprovechar la caché de Docker)
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente dentro del contenedor
COPY src /app/src

# Expone el puerto 8888 (útil si necesitas Jupyter)
EXPOSE 8888

CMD ["bash"]

