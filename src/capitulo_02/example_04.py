from gevent import monkey
monkey.patch_all()

import gevent
import time

def send_stat():
    time.sleep(0.001)
    
def do_thing(idx):
    print(f'{idx}: Primer Tarea')
    print(f'{idx}: Segunda Tarea')
    send_stat()
    print(f'{idx}: Tercer Tarea')
    
def do_things(idx):
    do_thing(idx)
    
gevent.joinall([gevent.spawn(do_things, x) for x in range(3)])