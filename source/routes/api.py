from fastapi.openapi.utils import get_openapi
from sqlalchemy.sql import text
from typing import Optional, List
from fastapi import FastAPI, Request


def access(db, table, method):
    return True


def init_app(app, sys, access_point="/api"):
    # define postgres,mysql as attributes of the object
    db = getattr(sys)

    @app.get(access_point, tags=[access_point])
    async def api():
        return True

    @app.get(access_point + "/{table}", tags=[access_point])
    async def get(table, request: Request):
        """all elements on a table"""
        return True

    async def get_list(statement, table):
        return True

    @app.post(access_point + "/{table}", tags=[access_point])
    async def post(table, request: Request):
        return True

    @app.put(access_point + "/{table}", tags=[access_point])
    async def put(table, request: Request):
        return True

    @app.delete(access_point + "/{table}", tags=[access_point])
    async def delete(table, request: Request):
        return True

    return app
