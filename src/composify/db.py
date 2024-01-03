# db
from sqlite3 import connect
import os
import asyncio
import asqlite

# custom utilities and setup
from . import log
log = log.Logger("db")

# Identify the location of the .config folder for composify
user_home = os.path.expanduser("~")
config_path = os.path.join(user_home, ".config", "composify")


DB_PATH = f"{config_path}/composify.db"
DB_SCRIPT = """
CREATE TABLE IF NOT EXISTS configuration(
    Project INTEGER PRIMARY KEY
);
"""

async def build():
    async with asqlite.connect(DB_PATH) as connection:
        async with connection.cursor() as cursor:
            await cursor.executescript(DB_SCRIPT)

            await log.info("Database built.")

async def commit():
    async with asqlite.connect(DB_PATH) as connection:
        await connection.commit()

        await log.info("Committed to database.")

async def close():
    async with asqlite.connect(DB_PATH) as connection:
        await connection.close()

        await log.info("Closed database connection.")

async def field(command, *values):
    async with asqlite.connect(DB_PATH) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(command, tuple(values))
            
            await log.info(f"Executed {command} with {values}.")

            if (fetch := await cursor.fetchone()) is not None: 
                await log.info(f"Fetched {fetch}.")
                return fetch[0]


async def record(command, *values):
    async with asqlite.connect(DB_PATH) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(command, tuple(values))

            await log.info(f"Executed {command} with {values}.")
            
            return await cursor.fetchone()

async def records(command, *values):
    async with asqlite.connect(DB_PATH) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(command, tuple(values))

            await log.info(f"Executed {command} with {values}.")

            return await cursor.fetchall()

async def column(command, *values):
    async with asqlite.connect(DB_PATH) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(command, tuple(values))

            await log.info(f"Executed {command} with {values}.")

            return [item[0] for item in await cursor.fetchall()]

async def execute(command, *values):
    async with asqlite.connect(DB_PATH) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(command, tuple(values))

            await log.info(f"Executed {command} with {values}.")

async def multiexec(command, valueset):
    async with asqlite.connect(DB_PATH) as connection:
        async with connection.cursor() as cursor:
            await cursor.executemany(command, valueset)

            await log.info(f"Executed {command} with {valueset}.")
