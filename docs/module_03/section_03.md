# Contruir un socket event loop

## Uso del módulo selector para crear un bucle de eventos de socket

Los sistemas operativos cuentan con APIs eficientes que nos permiten supervisar los sockets en busca de datos entrantes y otros eventos. Si bien la API en sí depende del sistema operativo (kqueue, epoll, IOCP, ...), todos estos sistemas de notificación de I/O que operan con un concepto similar. 

Les proporcionamos una lista de sockets que queremos monitorear en busca de eventos y, en lugar de verificar constantemente cada socket para ver si contiene datos, el sistema operativo nos indica explícitamente cuándo los sockets contienen datos.

Dado que esto se implementa a nivel de hardware, se utiliza muy poco la CPU durante esta monitorización, lo que permite un uso eficiente de los recursos. Estos sistemas de notificación son la base de cómo `asyncio` logra la concurrencia. 

Comprender cómo funciona esto nos da una visión de cómo funciona el sistema subyacente de asyncio.

Los sistemas de notificación de eventos varían según el sistema operativo.
Afortunadamente, el módulo de selectores de Python está abstraído, de modo que podemos obtener el evento adecuado para cualquier ejecución de nuestro código. Esto hace que nuestro código sea portátil entre diferentes sistemas operativos. Esta biblioteca expone una clase base abstracta llamada BaseSelector, que cuenta con múltiples implementaciones para cada sistema de notificación de eventos. También contiene una clase Selector Predeterminado, que selecciona automáticamente la implementación más eficiente para nuestro sistema.


