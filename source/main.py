import asyncio
import json
from typing import Optional, Any

import aioredis
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routes import doc, api
from classes.sys import SYS
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache import FastAPICache, JsonCoder
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

import os

sys = SYS()

# configure static and templates file on jinja 2
app = FastAPI(
    title=f"{sys.data['tool']['poetry']['name']}-{sys.env}",
    description=sys.data['tool']['poetry']['description'],
    version=sys.data['tool']['poetry']['version'],
    static_directory="static",
    docs_url=None,
    redoc_url=None
)


@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool(sys.redis, password="pass", encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = sys.delimiters(Jinja2Templates(directory="templates"))

doc.init_app(app, sys)
api.init_app(app, "/api")
api.init_app(app, "/safe")


@app.get("/", tags=["main"], response_class=HTMLResponse)
async def index(request: Request):
    data = {}
    if sys.debug == 'true':
        data = json.dumps(sys.decode(await index_data()))
        sys.logger(f"data-load-page:{data}", sys.log)
    return templates.TemplateResponse("index.html", {"request": request, "debug": sys.debug, "data": data,
                                                     "data_link": ['http://localhost:8080/index-data','http://localhost:8080/index-data2']})


def generate_key(
        func,
        namespace: Optional[str] = "",
        request: Request = None,
        response: Response = None,
        *args,
        **kwargs,
):
    prefix = FastAPICache.get_prefix()
    cache_key = f"Edson-{prefix}:{namespace}:{func.__module__}:{func.__name__}:{args}:{kwargs}"
    return cache_key


@app.get("/index-data", tags=["main"], response_class=HTMLResponse)
#@conditional_cache(int(os.getenv(f"CACHE[{sys.env}]")) != 0, cache(expire=int(os.getenv(f"CACHE[{sys.env}]")), coder=JsonCoder))
@cache(expire=10, coder=JsonCoder, key_builder=generate_key)
async def index_data():
    # await sys.await_time(5)
    data = {
        'i': [1],
        'v': [100]
    }
    if sys.debug == 'true':
        sys.logger(f"data:{data}", sys.log)
    return sys.encode(data)

@app.get("/index-data2", tags=["main"], response_class=HTMLResponse)
# @cond_decorator(int(os.getenv(f"CACHE[{sys.env}]")) != 0, cache(expire=int(os.getenv(f"CACHE[{sys.env}]")), coder=JsonCoder))
@cache(expire=10, coder=JsonCoder, key_builder=generate_key)
async def index_data2():
    # await sys.await_time(5)
    data = {
        'j': [2],
        'k': [200],
        'l': None
    }
    if sys.debug == 'true':
        sys.logger(f"data:{data}", sys.log)
    return sys.encode(data)


if __name__ == "__main__":
    sys.logger(f"Environment = {sys.env}", sys.log)
    uvicorn.run("main:app", host="localhost", port=8080, reload=os.getenv(f"DEBUG[{sys.env}]"), log_level="info")
