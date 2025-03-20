import gevent
from gevent.lock import RLock
from gevent import monkey
monkey.patch_all()
import time


rlock = RLock()


def task1():
    start_time = time.time()
    print(f"Task 1: trying to acquire the lock at {start_time}")
    with rlock:
        acquired_time = time.time()
        print(f"Task 1: acquired the lock at {acquired_time}, waited {acquired_time - start_time} seconds")
        gevent.sleep(1)
        
        print("Task 1: trying to re-acquire the lock")
        with rlock:
            re_acquired_time = time.time()
            print(f"Task 1.1: re-acquired the lock at {re_acquired_time}, time since last acquisition {re_acquired_time - acquired_time} seconds")
            gevent.sleep(5)
        with rlock:
            re_acquired_time = time.time()
            print(f"Task 1.2: re-acquired the lock at {re_acquired_time}, time since last acquisition {re_acquired_time - acquired_time} seconds")
            gevent.sleep(1)
        with rlock:
            re_acquired_time = time.time()
            print(f"Task 1.3: re-acquired the lock at {re_acquired_time}, time since last acquisition {re_acquired_time - acquired_time} seconds")
            gevent.sleep(1)
        with rlock:
            re_acquired_time = time.time()
            print(f"Task 1.4: re-acquired the lock at {re_acquired_time}, time since last acquisition {re_acquired_time - acquired_time} seconds")
            gevent.sleep(1)
        with rlock:
            re_acquired_time = time.time()
            print(f"Task 1.5: re-acquired the lock at {re_acquired_time}, time since last acquisition {re_acquired_time - acquired_time} seconds")
            gevent.sleep(1)
        print(f"Task 1: released the re-acquired lock at {time.time()}")
    print(f"Task 1: released the lock at {time.time()}")


def task2():
    gevent.sleep(0.5)
    start_time = time.time()
    print(f"Task 2: trying to acquire the lock at {start_time}")

    with rlock:
        acquired_time = time.time()
        print(f"Task 2: acquired the lock at {acquired_time}, waited {acquired_time - start_time} seconds")
    print(f"Task 2: released the lock at {time.time()}")


def main():
    g1 = gevent.spawn(task1)
    g2 = gevent.spawn(task2)
    gevent.joinall([g1, g2])


if __name__ == '__main__':
    main()