from gevent import pywsgi
from app import app
import multiprocessing


def start_server(port=8000):
    # Crear un servidor WSGI con gevent
    server = pywsgi.WSGIServer(('0.0.0.0', port), app)
    # Iniciar el servidor
    server.serve_forever()

if __name__ == '__main__':
    ports = [6000, 6001, 6002]
    processes = []
    for port in ports:
        p = multiprocessing.Process(target=start_server,, args=(port,))
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()