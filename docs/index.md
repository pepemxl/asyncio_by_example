# Introducción al computo asincrónico


Muchas aplicaciones aplicaciones web dependen en gran medida de operaciones de E/S (entrada/salida), I/O en ingles. Este tipo de operaciones incluyen la descarga de contenidos de una página web desde Internet, la comunicación a través de una red con un grupo de microservicios o la ejecución de varias consultas en conjunto en una base de datos como MySQL o Postgres. Un request o una llamada a un microservicio puede tardar cientos de milisegundos, o incluso segundos si la red es lenta. Una consulta a una base de datos puede requerir mucho tiempo. Un servidor web puede necesitar gestionar cientos o miles de solicitudes al mismo tiempo.

Realizar muchas de estas solicitudes de I/O a la vez puede provocar problemas de rendimiento. Si ejecutamos estas solicitudes una tras otra, como lo haríamos en una aplicación que se ejecuta de forma secuencial, veremos un impacto en el rendimiento. Por ejemplo, si estamos escribiendo una aplicación que necesita descargar 100 páginas web o ejecutar 100 consultas, cada una de las cuales tarda 1 segundo en ejecutarse, nuestra aplicación tardará al menos 100 segundos en ejecutarse. Sin embargo, si aprovecháramos la concurrencia e iniciáramos las descargas y la espera simultáneamente, en teoría, podríamos completar estas operaciones en tan solo 1 segundo.


Para resolver este tipo de problemas fue introducida la librería **asyncio**  en Python 3.4 y esta proyectado resolver los problemas del GIL para python 3.12 con lo cual el trabajar con soluciones hibridas entre concurrencia y paralelismo será posible en python.


Actualmente lo más común es usar multiprocessing con concurrencia en python. Por lo cual nos adentraremos en el desarollo de aplicaciones con python usando computo concurrente.



