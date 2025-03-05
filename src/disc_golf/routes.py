from aiohttp import web

async def get_discs(request):
    pool = request.app['db']
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM discs")
        return web.json_response([dict(row) for row in rows])

async def get_courses(request):
    pool = request.app['db']
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM courses")
        return web.json_response([dict(row) for row in rows])

async def get_scores(request):
    pool = request.app['db']
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM scores")
        return web.json_response([dict(row) for row in rows])

async def get_players(request):
    pool = request.app['db']
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM players")
        return web.json_response([dict(row) for row in rows])

def setup_routes(app):
    app.router.add_get('/discs', get_discs)
    app.router.add_get('/courses', get_courses)
    app.router.add_get('/scores', get_scores)
    app.router.add_get('/players', get_players)
