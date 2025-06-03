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