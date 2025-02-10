# asyncio by example



Para iniciar primero necesitaras habilitar un ambiente de trabajo, para ello usaremos contenedores de Docker.


1. Construye la imagen: `make build`
    ```bash
    ~/asyncio_by_example$ make build
    docker-compose build
    Building dev
    .
    .
    .
    => => naming to docker.io/library/asyncio_by_example_dev
    ```
2. Iniciar el contenedor: `make up`
    ```bash
    docker-compose up -d
    Creating network "asyncio_by_example_default" with the default driver
    Creating python_dev ... done
    ```
3. Para abrir una terminal dentro del contenedor: `make shell`
    ```bash
    docker exec -it python_dev bash
    root@2cea18f210d3:/app#
    ```
4. Para detener el contenedor: `make down`
5. Para eliminar el contenedor, imágenes y volúmenes: `make clean`


## Verificar que esta funcionando correctamente

Abre una terminal en VS Code dentro del contenedor y ejecuta:

```bash
make shell
python --version
```



## Conectar VSCode al contenedor

Una vez que el contenedor este corriendo (pasos 1 y 2)

1. Instala la extensión "Remote - Containers" en VS Code.
    - Si estas en WSL usa "Dev Containers"
2. Abre VS Code y presiona Ctrl + Shift + P (o Cmd + Shift + P en macOS).
3. Busca "Remote-Containers: Attach to Running Container".
    - Si estas en WSL usa "Dev Containers"
4. Selecciona el contenedor llamado `python_dev`.
5. Ahora puedes abrir archivos y ejecutar código desde el contenedor en VS Code.

