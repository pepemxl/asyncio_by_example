import asyncpg

DB_CONFIG = {
    "user": "postgres",
    "password": "password",
    "database": "disc_golf",
    "host": "localhost",
    "port": 5432
}

async def init_db():
    conn = await asyncpg.connect(**DB_CONFIG)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS discs (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            speed INTEGER,
            glide INTEGER,
            turn INTEGER,
            fade INTEGER
        )''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT,
            holes INTEGER
        )''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id SERIAL PRIMARY KEY,
            player_name TEXT NOT NULL,
            course_id INTEGER REFERENCES courses(id),
            total_score INTEGER,
            date_played DATE DEFAULT CURRENT_DATE
        )''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            pdga_number INTEGER UNIQUE,
            rating INTEGER,
            division TEXT
        )''')
    await conn.close()

async def create_pool():
    return await asyncpg.create_pool(**DB_CONFIG)
