# Introducción al computo asincrónico


Muchas aplicaciones aplicaciones web dependen en gran medida de operaciones de E/S (entrada/salida), I/O en ingles. Este tipo de operaciones incluyen:

- la descarga de contenidos de una página web desde Internet, 
- la comunicación a través de una red con un grupo de microservicios o 
- la ejecución de varias consultas en conjunto en una base de datos como MySQL o Postgres,
- y otras más.

Un request o una llamada a un microservicio puede tardar cientos de milisegundos, o incluso segundos si la red es lenta. Una consulta a una base de datos puede requerir mucho tiempo. Un servidor web puede necesitar gestionar cientos o miles de solicitudes al mismo tiempo.

Realizar muchas de estas solicitudes de I/O a la vez puede provocar problemas de rendimiento. Si ejecutamos estas solicitudes una tras otra, como lo haríamos en una aplicación que se ejecuta de forma secuencial, veremos un impacto en el rendimiento. Por ejemplo, si estamos escribiendo una aplicación que necesita descargar 100 páginas web o ejecutar 100 consultas, cada una de las cuales tarda 1 segundo en ejecutarse, nuestra aplicación tardará al menos 100 segundos en ejecutarse. Sin embargo, si aprovecháramos la concurrencia e iniciáramos las descargas y la espera simultáneamente, en teoría, podríamos completar estas operaciones en tan solo 1 segundo.


Para resolver este tipo de problemas fue introducida la librería **asyncio**  en Python 3.4 y esta proyectado resolver los problemas del GIL para python 3.12 con lo cual el trabajar con soluciones hibridas entre concurrencia y paralelismo será posible en python.


Actualmente lo más común es usar multiprocessing con concurrencia en python. Por lo cual nos adentraremos en el desarollo de aplicaciones con python usando computo concurrente.

Empezaremos con una de debian utilizando python 3.8 y más adelante migraremos a python 3.13, donde esperamos tener un framework más estable para multi-threading.


Para computo concurrente utilizaremos los siguientes paquetes.

- asyncio
- greenlets
- gevent


Para lograr todo esto debemos entender los siguientes conceptos:

1. Corrutinas,  del ingles Coroutines



## Coroutines

Las corrutinas en Python son funciones especiales que pueden pausar y reanudar su ejecución, lo que las hace muy adecuadas para la programación asincrónica. Estas son definidas mediante la sintaxis `async def`, las corrutinas permiten escribir código que realiza operaciones sin bloqueo. Dentro de una corrutina, la palabra clave `await` se utiliza para pausar la ejecución hasta que se complete una tarea determinada, lo que permite que otras corrutinas se ejecuten simultáneamente durante este período.


Coroutines
Coroutines in Python are special functions that can pause and resume their execution, making them highly suitable for asynchronous programming. Defined using the async def syntax, coroutines allow you to write code that performs non-blocking operations. Within a coroutine, the await keyword is used to pause execution until a given task is complete, enabling other coroutines to run concurrently during this period.

Event Loop
An event loop is a control structure that continuously cycles through a series of events, handling tasks and managing the flow of execution in a program. It waits for events to occur, processes them, and then moves on to the next event. This mechanism ensures that the program can respond to events, such as user input, timers, or messages, in an efficient and orderly manner.

HOW EVENT LOOP MANAGES COROUTINES
Task Submission:When you submit a coroutine to the event loop, it is typically wrapped in a Task object. This task is then scheduled to run on the event loop.
Internal Queues: The event loop uses several internal data structures, including queues, to manage and schedule these tasks:
Ready Queue: Contains tasks that are ready to run immediately.
I/O Selector: Monitors file descriptors and schedules tasks based on I/O readiness.
Scheduled Callbacks: Manages tasks that are scheduled to run after a certain delay.
3. Scheduling: The event loop continuously checks these queues and data structures to determine which tasks are ready to execute. It then runs the tasks, handling await statements by pausing and resuming them as necessary.

4. Concurrency Management: By interleaving the execution of multiple coroutines, the event loop achieves concurrency without the need for multiple threads.

At any point, only one task will be running, but it switches to another task if one task is I/O bound, giving the illusion of parallelism.

ASYNCIO IN ACTION
import asyncio
import time

async def task1():
    print("Task 1 started")
    await asyncio.sleep(1)  # Yield control to the event loop
    print("Task 1 resumed")
    await asyncio.sleep(1)  # Yield control to the event loop

async def task2():
    print("Task 2 started")
    await asyncio.sleep(1)  # Yield control to the event loop
    print("Task 2 resumed")
    await asyncio.sleep(1)  # Yield control to the event loop

async def main():
    await asyncio.gather(task1(), task2())

start_time = time.time()
asyncio.run(main())
end_time = time.time()

print(f"Total time: {end_time - start_time:.2f} seconds")

'''
Task 1 starts and yields control with await asyncio.sleep(1).
Task 2 starts and yields control with await asyncio.sleep(1).
After 1 second, both tasks resume.
Task 1 resumes and yields control with await asyncio.sleep(1).
Task 2 resumes and yields control with await asyncio.sleep(1).
After another second, both tasks finish.
Total time taken is 2 sec.
'''
With the above example we can see how we can benifit switching task for i/o operation. The same logic sequencially would take 4 sec but with asyncio we can definitely reduce the time by straight half.

In the provided code, the event loop acts like a manager running on a single thread. It keeps track of tasks like task1 and task2, making sure they get their turn to run. The CPU processes these tasks one by one, but when a task is waiting for something (like a pause with await asyncio.sleep), it hands over control to the event loop. This allows the event loop to switch to the other task that's ready to run. This way, even though everything happens in one thread, tasks are executed efficiently and concurrently without having to wait for each other to finish completely.

SOME ASYNCIO TERMINOLOGIES
asyncio.run(coro):

Runs the main coroutine coro and manages the event loop. It creates a new event loop, runs the coroutine until it finishes, and then closes the loop.
It is designed to be used outside of asynchronous functions and is typically called at the entry point of your program.
Can’t be run inside an existing event loop.
asyncio.create_task(coro):

Schedules the coroutine coro to run concurrently and returns a Task object. This function is useful for starting multiple coroutines and managing them.
This command required an existing event loop for it’s execution.
Used to start a coroutine that should run concurrently with other tasks. It is ideal for tasks that need to run in parallel with other asynchronous operations.
asyncio.gather(*coros):

Runs multiple coroutines concurrently and waits for all of them to complete. It collects their results into a list.
Requires an active event loop for managing coroutines.
event_loop.run_until_complete(coro):

Runs a coroutine until it completes using an existing event loop. It blocks until the coroutine finishes and returns the result.
It not meant to be used inside an asynchronous function. It is intended for running a coroutine until it completes, but should be used outside async functions, typically in synchronous contexts.
Fun Exercise
This code will let you know a bit more about how event loop works.

import asyncio
import time

async def sleeping_task():
    print("sleeping task started")
    await asyncio.sleep(2)
    print("sleeping task completed")

async def main():
    start_time = time.time() 
    task = asyncio.create_task(sleeping_task())
    print("Main function is running")
    # await task (await at position one before main i/o operation)
    await asyncio.sleep(1) 
    # await task ( await at position two after main i/o opearation)

    end_time = time.time()
    print("Main function completed")
    print(f"Total time for main function: {end_time - start_time:.2f} seconds")

asyncio.run(main())
Can you guess what’s the difference in time will get if we use await task before and after asyncio.sleep().

Case 1: Awaiting task Before await asyncio.sleep(1)
Event Loop Starts:

The event loop starts running when asyncio.run(main()) is called.

Create and Schedule Task:

asyncio.create_task(sleeping_task()) schedules sleeping_task to run in the background. The event loop starts running sleeping_task concurrently with main.

Await Task:

await task waits for sleeping_task to complete. This takes 2 seconds because sleeping_task is sleeping for 2 seconds.

Await Additional Sleep:

Once sleeping_task completes, the main function then performs await asyncio.sleep(1), which adds an additional 1-second wait.

Total Time:

2 seconds (for sleeping_task to complete) + 1 second (for await asyncio.sleep(1)) = 3 seconds.

Case 2: Awaiting task After await asyncio.sleep(1)
Event Loop Starts:

The event loop starts running when asyncio.run(main()) is called.

Create and Schedule Task:

asyncio.create_task(sleeping_task()) schedules sleeping_task to run in the background.

Await Sleep:

await asyncio.sleep(1) makes the main coroutine wait for 1 second. During this time, sleeping_task is running concurrently in the event loop.

Await Task:

After 1 second, the main function waits for sleeping_task to complete using await task. Since sleeping_task needs an additional 1 second to complete (totaling 2 seconds), it will complete after the remaining 1 second.

Total Time:

1 second (for await asyncio.sleep(1)) + 1 second (remaining time for sleeping_task to complete) = 2 seconds.

With the above example we can also see that child execution is independent of parent function.

When a sub-task is created within a task, the event loop manages the sub-task as an independent entity. This means that both the parent task and the sub-task are handled concurrently and independently by the event loop, allowing for efficient execution and resource management.

Not we have basic understanding of asyncio let’s move on to greenlets than compare the use cases for which each is suitable.

GREENLETS AND GEVENT IN PYTHON
Coroutines and greenlets(green threads) are both mechanisms for managing concurrent execution in Python, but they have distinct differences in terms of implementation, control, and use cases.

Greenlets are a low-level, user-space coroutine implementation provided by the greenlet library in Python.

from greenlet import greenlet
import time

def task1():
    start_time = time.time()
    print("Task 1 started")
    time.sleep(1)  # Simulate work
    print("Task 1 yielding")
    gr2.switch()  # Yield control to task2
    print("Task 1 resumed")
    time.sleep(1)  # Simulate more work
    end_time = time.time()
    print(f"Task 1 completed in {end_time - start_time:.2f} seconds")

def task2():
    start_time = time.time()
    print("Task 2 started")
    time.sleep(1)  # Simulate work
    print("Task 2 yielding")
    gr1.switch()  # Yield control to task1
    print("Task 2 resumed")
    time.sleep(1)  # Simulate more work
    end_time = time.time()
    print(f"Task 2 completed in {end_time - start_time:.2f} seconds")

# Create greenlets
gr1 = greenlet(task1)
gr2 = greenlet(task2)

# Start task1 and switch to task2
start_time = time.time()
gr1.switch()
gr2.switch()
end_time = time.time()

print(f"Total execution time: {end_time - start_time:.2f} seconds")


"""
Here task 1 and task 2 each take 3 sec and overall programm gets completed
in 4 sec. We can easily interpret it by going line by line throught code.
Were you expecting it to be 2 sec :).
"""
Greenlet provide full flexibility to user for switching different execution contexts in a cooperative multitasking manner. It lacks build-in support for asynchronous I/O operations.

Don’t worry we have gevent for our rescue.

Gevent is a higher-level library built on Greenlet, providing built-in support for non-blocking I/O and higher-level abstractions, suitable for I/O-bound applications.

Gevent abstracts away the complexity of context switching and provides built-in support for non-blocking I/O operations.

import gevent
import time

def task1():
    print("Task 1 started")
    gevent.sleep(1)
    print("Task 1 resumed")
    gevent.sleep(1)

def task2():
    print("Task 2 started")
    gevent.sleep(1)
    print("Task 2 resumed")
    gevent.sleep(1)

start_time = time.time()

# Create greenlets
g1 = gevent.spawn(task1)
g2 = gevent.spawn(task2)

# Start greenlets and wait for them to complete
gevent.joinall([g1, g2])

end_time = time.time()

print(f"Total time: {end_time - start_time:.2f} seconds")

"""
 Now this takes two second
"""
Considering speed as the benchmark, we’ll set aside greenlet for now, as implementing functionality that gevent already provides would be time-consuming and beyond the scope of this blog. We’ll focus on comparing gevent and asyncio moving forward.

1. Event Loop Management:

Gevent: Manages its own event loop and relies on monkey patching to make standard I/O operations asynchronous. This means that it modifies the behavior of standard library modules to support its concurrency model.
Asyncio: Includes a built-in event loop that is part of Python’s standard library. It provides native support for managing asynchronous operations without requiring monkey patching.
2. Monkey Patching:

Gevent: Requires explicit monkey patching to convert blocking I/O operations into non-blocking ones. This involves modifying standard library modules to integrate with gevent's event loop.
Asyncio: Does not require monkey patching. It uses Python’s native async/await functionality, which integrates seamlessly with the standard library’s asynchronous I/O operations.
3. Performance:

Gevent: Efficient for I/O-bound tasks, particularly in systems where monkey patching is already used. It can add overhead due to the need for monkey patching but is still effective in many scenarios.
Asyncio: Generally provides high performance with native support for asynchronous programming. It is optimized for modern applications and offers efficient handling of I/O-bound tasks without the overhead of monkey patching.
4. Error Handling:

Gevent: May require careful management of exceptions due to the use of monkey-patched libraries. Error handling needs to be managed within the greenlets.
Asyncio: Utilizes standard Python error handling within coroutines. The native syntax makes it easier to handle exceptions in asynchronous code.
5. Use Cases:

Gevent: Ideal for integrating asynchronous behavior into existing synchronous codebases or when working with libraries compatible with greenlets. It’s suitable for applications that need to patch existing I/O operations to be asynchronous.
Asyncio: Best for new applications or codebases that adopt modern asynchronous programming practices. It’s well-suited for high-performance network applications and I/O-bound tasks that benefit from native async support.
Asyncio is typically chosen for new applications where modern asynchronous programming practices are preferred. It integrates seamlessly with Python’s standard library and is well-suited for network applications, real-time communication, and services requiring high concurrency.

Gevent is often chosen for existing synchronous codebases that need to be adapted to support concurrency. Its ability to monkey-patch standard library modules makes it a good fit for applications that need to convert blocking I/O operations into non-blocking ones, such as in web servers, chat applications, and real-time systems.

BONUS MATERIAL
Let’s look at some real world examples that uses asyncio and gevents.

Web Servers:
FastAPI: Although primarily built on Starlette and Pydantic, FastAPI leverages asyncio for handling asynchronous requests, making it a high-performance web framework for building APIs.
Gunicorn with gevent workers: A popular WSGI HTTP server for Python applications, which can use gevent workers to handle a large number of simultaneous connections efficiently.
Flask with gevent: Although Flask itself is synchronous, combining it with gevent allows handling multiple requests concurrently, making it suitable for real-time applications.
Real-time Communication:
Discord.py: An API wrapper for Discord that uses asyncio to handle real-time events and interactions efficiently.
Networking Tools:
AsyncSSH: A library for SSHv2 protocol implementation, providing asynchronous APIs for working with SSH, SFTP, and SCP, built on top of asyncio.
ZeroMQ with gevent: For applications requiring high-performance messaging, gevent is often used with ZeroMQ to handle asynchronous communication patterns effectively.
Database Access:
Gevent with SQLAlchemy: For applications requiring asynchronous database access, combining gevent with SQLAlchemy allows handling database queries without blocking the main thread.