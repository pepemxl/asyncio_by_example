import time


def tarea():
    print("Inicio de tarea")
    time.sleep(2)
    print("Tarea completada")

def main():
    tarea()
    tarea()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print("Tiempo usado: ", end-start)