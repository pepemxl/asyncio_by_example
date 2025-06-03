import time
import threading
import requests


def read_example() -> None:
    response = requests.get('https://www.google.com.mx')
    print(response.status_code)

def test_synchronous():
    start = time.time()
    read_example()
    read_example()
    end = time.time()
    print(f'Sincrono tomo {end - start:.4f} segundos.')

def test_asynchronous():
    thread_1 = threading.Thread(target=read_example)
    thread_2 = threading.Thread(target=read_example)
    thread_start = time.time()
    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()
    thread_end = time.time()
    print(f'Asincrono tomo {thread_end - thread_start:.4f} Segundos.')


if __name__ == '__main__':
    test_synchronous()
    test_asynchronous()