from gevent import pywsgi
from app import app


def start_server(port=8000):
    # Crear un servidor WSGI con gevent
    server = pywsgi.WSGIServer(('0.0.0.0', port), app)
    # Iniciar el servidor
    server.serve_forever()

if __name__ == '__main__':
    start_server()
