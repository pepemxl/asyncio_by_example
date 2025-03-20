from gevent import monkey
monkey.patch_all()
import gevent
import time

def fetch_resource(result, response_time=0.01):
    gevent.sleep(response_time)
    return result
    
def compute_thing():
    a = fetch_resource(1)
    b = fetch_resource(2)
    c = fetch_resource(3)
    return a + b + c

def compute_thing_parallel():
    tasks = [
        gevent.spawn(fetch_resource, 1),
        gevent.spawn(fetch_resource, 2),
        gevent.spawn(fetch_resource, 3)
    ]
    a, b, c = [t.get() for t in  gevent.joinall(tasks)]
    return a + b + c

def main():
    list_times = []
    N_iterations = 10
    suma = 0
    for i in range(N_iterations):
        start = time.time()
        compute_thing_parallel()
        end = time.time()
        time_elapsed = end-start
        list_times.append(time_elapsed)
        suma += time_elapsed
    avg_time = suma/N_iterations
    print(f"Tiempo promedio {avg_time} segs")


if __name__ == '__main__':
    main()