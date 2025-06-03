# Procesos e Hilos


## Procesos

Un **proceso** es una aplicación que se ejecuta y tiene un espacio de memoria al que otras aplicaciones no pueden acceder. 

Varios procesos pueden ejecutarse en una sola máquina. Si usamos una máquina con una CPU de varios núcleos, podemos ejecutar varios procesos simultáneamente. Si usamos una CPU de un solo núcleo, podemos tener varias aplicaciones ejecutándose simultáneamente mediante la segmentación de tiempo. Cuando un sistema operativo utiliza la segmentación de tiempo, cambia automáticamente entre los procesos en ejecución después de un tiempo.

Los algoritmos que determinan cuándo se produce este cambio varían según el sistema operativo.

```python title="Procesos e Hilos" linenums="1"
import threading


def hello_from_thread():
    print(f'Hola desde el hilo {threading.current_thread()}!')

def test_threading():
    hello_thread = threading.Thread(target=hello_from_thread)
    hello_thread.start()
    total_threads = threading.active_count()
    thread_name = threading.current_thread().name
    print(f'Python esta corriendo {total_threads} hilo(s)')
    print(f'Hilo actual {thread_name}')
    hello_thread.join()


if __name__ == '__main__':
    test_threading()
```

```python title="Salida de multiples ejecuciones"
root@adafb481d2b7:/app# /usr/local/bin/python /app/src/capitulo_01/section_01/multithread.py
Hola desde el hilo <Thread(Thread-1 (hello_from_thread), started 131578161936064)>!
Python esta corriendo 2 hilo(s)
Hilo actual MainThread
root@adafb481d2b7:/app# /usr/local/bin/python /app/src/capitulo_01/section_01/multithread.py
Hola desde el hilo <Thread(Thread-1 (hello_from_thread), started 134282509616832)>!
Python esta corriendo 2 hilo(s)
Hilo actual MainThread
root@adafb481d2b7:/app# /usr/local/bin/python /app/src/capitulo_01/section_01/multithread.py
Hola desde el hilo <Thread(Thread-1 (hello_from_thread), started 130133606295232)>!
Python esta corriendo 2 hilo(s)
Hilo actual MainThread
root@adafb481d2b7:/app# /usr/local/bin/python /app/src/capitulo_01/section_01/multithread.py
Hola desde el hilo <Thread(Thread-1 (hello_from_thread), started 135540787914432)>!
Python esta corriendo 2 hilo(s)
Hilo actual MainThread
```

Creamos un método para imprimir el nombre del hilo actual y luego creamos un hilo para ejecutar ese método. Después, llamamos al método de inicio del hilo para iniciar su ejecución. Finalmente, llamamos al método de unión (`join`). Esta acción pausará el programa hasta que el hilo que iniciamos se complete.

## Hilos

Los **hilos** pueden considerarse **procesos** más ligeros. Además, son la construcción más pequeña que puede gestionar un sistema operativo. No tienen memoria propia como un proceso; comparten la memoria del proceso que los creó. Los hilos están asociados al proceso que los creó. Un proceso siempre tendrá al menos un hilo asociado, generalmente conocido como **hilo principal**. Un proceso también puede crear otros hilos, más comúnmente conocidos como hilos de trabajo o en segundo plano. Estos hilos pueden realizar otras tareas simultáneamente junto con el hilo principal. Los hilos, al igual que los procesos, pueden ejecutarse simultáneamente en una CPU multinúcleo, y el sistema operativo también puede alternar entre ellos mediante la segmentación de tiempo.

Cuando ejecutamos una aplicación Python normal, creamos un proceso y un hilo principal que se encargará de ejecutar nuestra aplicación Python.


```python title="Procesos e Hilos" linenums="1"
import os
import threading

def print_thread_details():
    print(f'Este proceso de Python corren con el id: {os.getpid()}')
    total_threads = threading.active_count()
    thread_name = threading.current_thread().name
    print(f'Python esta corriendo {total_threads} hilos')
    print(f'El hilo actual es {thread_name}')

if __name__ == '__main__':
    print_thread_details()
```

```python title="Salida"
Este proceso de Python corren con el id: 84736
Python esta corriendo 1 hilos
El hilo actual es MainThread
```

Cada vez que lo ejecutamos se actualiza el `id` de hilo corriendo el programa.
