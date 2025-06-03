import multiprocessing
import os


def hello_from_process():
    print(f'Hola desde el proceso hijo {os.getpid()}')

def test_multiprocess():
    hello_process = multiprocessing.Process(target=hello_from_process)
    hello_process.start()
    print(f'Hola desde el proceso padre {os.getpid()}')
    hello_process.join()

if __name__ == '__main__':
    test_multiprocess()