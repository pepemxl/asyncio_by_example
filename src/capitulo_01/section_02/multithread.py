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