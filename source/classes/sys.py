import asyncio
from fastapi_cache.decorator import cache
from fastapi_cache import JsonCoder
from stuf import stuf
import dataset
import toml
from pathlib import Path
import os
import dotenv
import logging
from datetime import datetime

from fastapi.logger import logger



def conditional_cache(flag):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            return await cache(coder=JsonCoder)(func)(*args, **kwargs) if flag else await func()
        return wrapper
    return decorator

class SYS:
    dotenv.load_dotenv()
    logger = logging.getLogger(__name__)

    def __init__(self):
        toml_file = Path('../source/pyproject.toml').read_text()
        self.data = toml.loads(toml_file)
        self.env = os.getenv(f"ENV")
        self.exp = os.getenv(f"EXP")
        self.debug = os.getenv(f"DEBUG[{self.env}]")
        self.redis = os.getenv(f"REDIS_DOCKER[{self.env}]")
        self.log = os.getenv(f"DEBUG-LEVEL[{self.env}]")
        self.postgres = self.__connect(os.getenv(f"POSTGRES_URI[{self.env}]"))
        self.mysql = None

    def __connect(self, url="postgresql://postgres:668262aZ@localhost:5432"):
        ...

    def logger(self, msg, level="info"):
        if level == "info":
            logger.info(f"{level.upper()}[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]: {msg}")
        if level == "warning":
            logger.warning(f"{level.upper()}[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]: {msg}")

    def delimiters(self, template):
        template.env.block_start_string = "[%"
        template.env.block_end_string = "%]"
        template.env.variable_start_string = "[["
        template.env.variable_end_string = "]]"
        return template

    def env_is(self, env):
        return self.env == env

    def env_not(self, env):
        return self.env != env

    async def await_time(self, time):
        await asyncio.sleep(time)

    def encode(self, data):
        return JsonCoder().encode(data)

    def decode(self, data):
        return JsonCoder().decode(data)