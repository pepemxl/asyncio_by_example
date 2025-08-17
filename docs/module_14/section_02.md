# Gevent + Asyncio

Para poder empezar a trabajar asyncio con proyectos desarollados originalmente con gevent, tenemos librerias como gevent_asyncio que crea puentes entre ambos frameworks.


## Gevent a fondo


Gevent ofrece una biblioteca de redes de Python basada en corrutinas que utiliza multitarea cooperativa para proporcionar una API síncrona sobre E/S asíncrona.


gevent permite escribir aplicaciones de red asíncronas utilizando patrones de programación síncrona conocidos. Esto se logra mediante tres mecanismos principales:

- Multitarea cooperativa mediante greenlets (hilos ligeros y cooperativos)
- E/S basada en eventos mediante backends libev o libuv
- Aplicación de parches para que los módulos de la biblioteca estándar sean compatibles con gevent


Esta biblioteca permite a los desarrolladores escribir código que parece síncrono pero se ejecuta de forma asíncrona, cediendo automáticamente el control durante las operaciones de E/S sin necesidad de devoluciones de llamadas explícitas ni sintaxis async/await.


### Descripción general de la arquitectura del sistema


`gevent` sigue una arquitectura en capas donde las aplicaciones interactúan con módulos de biblioteca estándar parcheados por Monkey o con la API directa de gevent, los cuales se coordinan a través de un bucle de eventos central y un sistema de gestión de greenlets.


```mermaid
---
config:
  theme: redux
  layout: elk
---
flowchart TD
 subgraph subGraph0["I/O Subsystems"]
        StreamServer["StreamServer<br>DatagramServer"]
        WSGIServer["WSGIServer"]
        DNSResolvers["DNSResolvers"]
  end
 subgraph subGraph1["Application Layer"]
        StandardLibrary["Standard Library<br>Monkey Patched"]
        ApplicationCode["Application Code"]
  end
 subgraph subGraph2["Public API Layer"]
        geventThreading["gevent.threading"]
        geventQueue["gevent.queue"]
        geventSocket["gevent.socket"]
        geventGreenlet["gevent.Greenlet"]
        geventSubprocess["gevent.subprocess"]
  end
 subgraph subGraph3["Core Runtime"]
        Synchronization["Syncrhonization<br>Event, Semaphore, Lock"]
        Hub["Hub<br>(Event Loop Manager)"]
        geventLocal["gevent.local<br>(Task-local Storage)"]
  end
 subgraph subGraph4["Event Loop Backends"]
        CFFIBridge["CFFIBridge"]
        LibevBackend["LibevBackend"]
        LibuvBackend["LibuvBackend"]
  end
    WSGIServer --> StreamServer
    ApplicationCode --> StandardLibrary & geventSocket & geventGreenlet
    StandardLibrary --> geventSocket
    geventThreading --> geventGreenlet
    Synchronization --> Hub
    geventGreenlet --> geventLocal & Hub
    geventQueue --> Synchronization
    LibevBackend --> CFFIBridge
    LibuvBackend --> CFFIBridge
    Hub --> LibevBackend & LibuvBackend
    StreamServer --> geventSocket
    geventSocket --> DNSResolvers & Hub
    geventSubprocess --> Hub
    style StreamServer fill:#468c98,stroke:#fff,stroke-width:2px
    style WSGIServer fill:#468c98,stroke:#fff,stroke-width:2px
    style DNSResolvers fill:#468c98,stroke:#fff,stroke-width:2px
    style StandardLibrary fill:#9370db,stroke:#fff,stroke-width:2px
    style ApplicationCode fill:#468c98,stroke:#fff,stroke-width:2px
    style geventThreading fill:#9370db,stroke:#000,stroke-width:2px
    style geventQueue fill:#9370db,stroke:#000,stroke-width:2px
    style geventSocket fill:#9370db,stroke:#000,stroke-width:2px
    style geventGreenlet fill:#9370db,stroke:#fff,stroke-width:2px
    style geventSubprocess fill:#9370db,stroke:#000,stroke-width:2px
    style Synchronization fill:#9370db,stroke:#000,stroke-width:2px
    style Hub fill:#9370db,stroke:#000,stroke-width:2px
    style geventLocal fill:#9370db,stroke:#000,stroke-width:2px
    style CFFIBridge fill:#ff5588,stroke:#000,stroke-width:2px
    style LibevBackend fill:#ff5588,stroke:#000,stroke-width:2px
    style LibuvBackend fill:#ff5588,stroke:#000,stroke-width:2px
```















