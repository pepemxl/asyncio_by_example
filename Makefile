# Nombre del contenedor
CONTAINER_NAME=python_dev

PYTHON_VERSION = 3.11
TEST_PATH = tests/
REPORTS_DIR = reports

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

test-async:
#	pytest -p pytest_gevent_patch -asyncio-mode=auto
	pytest -p pytest_gevent_patch --gevent-patch -asyncio-mode=auto
#	Activa el monkey patch
#	pytest -p pytest_gevent_patch --gevent-patch tests/

test:
	docker exec -pytest tests/

test-docker:
	@mkdir -p $(REPORTS_DIR)
	docker run --rm \
		-v $(PWD):/app \
		-w /app \
		-e PYTHONPATH=/app \
		python:$(PYTHON_VERSION) \
		sh -c "pytest -p pytest_gevent_patch --gevent-patch -asyncio-mode=auto \
			--junitxml=$(REPORTS_DIR)/junit.xml \
			$(TEST_PATH)"