# Usa una imagen oficial de Python
FROM python:3.11

# Fija el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias del sistema (necesarias para Cap'n Proto)
RUN apt-get update && apt-get install -y \
    build-essential \
    #capnproto \
    libcapnp-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia solo el archivo de dependencias primero (para aprovechar la caché de Docker)
COPY requirements.txt .

# Actualiza pip
RUN  pip install --upgrade pip
# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install asyncio-gevent==0.2.3
#RUN pip install pycapnp==1.1.0
# Copia el código fuente dentro del contenedor
COPY src /app/src

# Expone el puerto 8888 (útil si necesitas Jupyter)
EXPOSE 8888
EXPOSE 8000
EXPOSE 5000

# Este ccontenedor es desarrollo asi que estaremos usando solo bash
CMD ["bash"]
# Comando para ejecutar la aplicación Flask
#CMD ["flask", "run", "--host=0.0.0.0"]

