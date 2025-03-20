import gevent
from gevent import monkey

# Aplica el monkey patching para hacer que las operaciones de E/S sean asíncronas.
monkey.patch_all()

import requests
import datetime

def fetch(url):
    now = datetime.datetime.now()
    print(f"Iniciando solicitud a {url}", now)
    response = requests.get(url)
    now = datetime.datetime.now()
    print(f"Respuesta de {url}: {len(response.content)} bytes", now)

# Crea tareas asíncronas (greenlets).
greenlets = [
    gevent.spawn(fetch, "https://www.example.com"),
    gevent.spawn(fetch, "https://www.google.com"),
    gevent.spawn(fetch, "https://www.github.com"),
    gevent.spawn(fetch, "https://www.google.com"),
    gevent.spawn(fetch, "https://www.google.com"),
    gevent.spawn(fetch, "https://www.google.com"),
    gevent.spawn(fetch, "https://www.google.com"),
    gevent.spawn(fetch, "https://www.google.com"),
    gevent.spawn(fetch, "https://www.google.com"),
]

# Espera a que todas las tareas terminen.
gevent.joinall(greenlets)