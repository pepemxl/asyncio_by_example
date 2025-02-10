# Nombre del contenedor
CONTAINER_NAME=python_dev

# Construir la imagen con docker-compose
build:
	docker-compose build

# Levantar el contenedor en segundo plano
up:
	docker-compose up -d

# Conectar al contenedor con una terminal interactiva
shell:
	docker exec -it $(CONTAINER_NAME) bash

# Parar el contenedor
down:
	docker-compose down

# Eliminar el contenedor y la imagen
clean:
	docker-compose down --rmi all --volumes --remove-orphans
