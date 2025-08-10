PY := python3.11
PYTHON_VERSION = 3.11
VENV := venv
REPONAME=$(basename $(pwd))
DOCKER=docker
DOCKER_COMPOSE = docker-compose


# Nombre del contenedor de pruebas
CONTAINER_NAME=python_dev

TEST_PATH = tests/
REPORTS_DIR = reports

.PHONY: build up down restart clean watch compile
.PHONY: build_docs up_docs down_docs restart_docs clean_docs


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


############# Docs ############
DOCKERFILE_DIR_DOCS := ./src/containers/docs
IMAGE_NAME_DOCS := asyncio-docs
CONTAINER_NAME_DOCS := asyncio-docs
PORT_DOCS := 8080

# Construye la imagen Docker usando el Dockerfile en /src/containers/docs/
build_docs:
	$(DOCKER) build -t $(IMAGE_NAME_DOCS) -f $(DOCKERFILE_DIR_DOCS)/Dockerfile .

# Levanta el contenedor y expone el puerto 8080 (con live-reload y montado de volumen)
run_docs:
#	 $(DOCKER) run --rm -it -p $(PORT_DOCS):$(PORT_DOCS) -v $(PWD):/app $(IMAGE_NAME_DOCS)
	$(DOCKER) run --rm -it \
		--name $(CONTAINER_NAME_DOCS) \
		-p $(PORT_DOCS):$(PORT_DOCS) \
		-v $(PWD):/app \
		$(IMAGE_NAME_DOCS)

# Detiene y elimina el contenedor (si está en segundo plano)
clean_docs:
	$(DOCKER) stop $(CONTAINER_NAME_DOCS) || true
	$(DOCKER) rm $(IMAGE_NAME_DOCS) || true

# Atajo para build + run
up_docs: build_docs run_docs



################# LOCAL  ENVIRONMENT ############################

${VENV}:
	@echo "Create venv"
	${PY} -m venv ./${VENV}
	@echo "Update pip"
	./${VENV}/bin/python3 -m pip install --upgrade pip
#	./${VENV}/bin/pip install poetry
	./${VENV}/bin/pip install -r requirements.txt
#	./${VENV}/bin/poetry install

.PHONY: local_env
local_env: $(VENV)
	@echo "Installed project in virtual environment..."
	@echo "Linux: Use \"source venv/bin/activate\""
#	@echo "Linux: Run \"poetry install\""
	@echo ${REPONAME}

.PHONY: clean_local_env
clean_local_env: ${VENV}
	rm -rf dist
	rm -rf ${VENV}
	rm -rf poetry.lock
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete

.PHONY: clean_local_env_cache
clean_local_env_cache: ${VENV}
	find . -type f -name *.pyc -delete
	ind . -type d -name __pycache__ -delete