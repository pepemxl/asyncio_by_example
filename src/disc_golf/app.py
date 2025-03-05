from aiohttp import web
import asyncio
import asyncpg

from db import init_db, create_pool
from routes import setup_routes

async def create_app():
    app = web.Application()
    
    # Configurar rutas
    setup_routes(app)
    
    # Configurar conexión a la base de datos
    app['db'] = await create_pool()
    
    return app

loop = asyncio.get_event_loop()
loop.run_until_complete(init_db())
app = loop.run_until_complete(create_app())

if __name__ == '__main__':
    web.run_app(app)
