# db
from sqlite3 import connect
import os
import asyncio
import asqlite

# custom utilities and setup
from . import log

class DB:
    """
    Database class.
    """
    log = log.Logger("db")
    DB_PATH="" # NOTE: The DB_PATH is defined in a classmethod below!
    DB_SCRIPT = """
    CREATE TABLE IF NOT EXISTS projects(
        PROJECT TEXT NOT NULL,
        HASH VARCHAR(8) UNIQUE NOT NULL,
        DESCRIPTION TEXT NOT NULL,
        PRIMARY KEY (project, hash)
    );
    """

    def __init__(self):
        pass

    @classmethod
    async def initialize(cls, dev):
        if dev:
            config_path = os.path.join(".dev")
            cls.DB_PATH=f"{config_path}/composify.dev.db"
        else:
            user_home = os.path.expanduser("~")
            config_path = os.path.join(user_home, ".config", "composify")
            cls.DB_PATH = f"{config_path}/composify.db"
        
        async with asqlite.connect(cls.DB_PATH) as connection:
            async with connection.cursor() as cursor:
                await cursor.executescript(cls.DB_SCRIPT)

                await cls.log.info("Database built.")

    @classmethod
    async def commit(cls):
        async with asqlite.connect(cls.DB_PATH) as connection:
            await connection.commit()

            await cls.log.info("Committed to database.")

    @classmethod
    async def close(cls):
        async with asqlite.connect(cls.DB_PATH) as connection:
            await connection.close()

            await cls.log.info("Closed database connection.")

    @classmethod
    async def field(cls, command, *values):
        async with asqlite.connect(cls.DB_PATH) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(command, tuple(values))
                
                await cls.log.info(f"Executed {command} with {values}.")

                if (fetch := await cursor.fetchone()) is not None: 
                    await cls.log.info(f"Fetched {fetch}.")
                    return fetch[0]

    @classmethod
    async def record(cls, command, *values):
        async with asqlite.connect(cls.DB_PATH) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(command, tuple(values))

                await cls.log.info(f"Executed {command} with {values}.")
                
                return await cursor.fetchone()

    @classmethod
    async def records(cls, command, *values):
        async with asqlite.connect(cls.DB_PATH) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(command, tuple(values))

                await cls.log.info(f"Executed {command} with {values}.")

                return await cursor.fetchall()

    @classmethod
    async def column(cls, command, *values):
        async with asqlite.connect(cls.DB_PATH) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(command, tuple(values))

                await cls.log.info(f"Executed {command} with {values}.")

                return [item[0] for item in await cursor.fetchall()]

    @classmethod
    async def execute(cls, command, *values):
        async with asqlite.connect(cls.DB_PATH) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(command, tuple(values))

                await cls.log.info(f"Executed {command} with {values}.")

    @classmethod
    async def multiexec(cls, command, valueset):
        async with asqlite.connect(cls.DB_PATH) as connection:
            async with connection.cursor() as cursor:
                await cursor.executemany(command, valueset)

                await cls.log.info(f"Executed {command} with {valueset}.")
