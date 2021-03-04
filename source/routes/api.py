from fastapi.openapi.utils import get_openapi
from sqlalchemy.sql import text
from typing import Optional, List
from fastapi import FastAPI, Request


def access(db, table, method):
    if table is not None and db['apis'].count(table=table) > 0 and list(db['apis'].find(table=table))[0][method]:
        return True
    else:
        # fix after test
        return False


def anti_injection(params):
    words = ["$", "*", "SELECT", "DROP"]
    for w in words:
        params = params.replace(w, "")
    return params


async def url_query(request):
    params = anti_injection(request.url.query)
    statement = params.replace("&", " AND ").replace("%22", "") \
        .replace("%27", "'").replace("|", " OR ").replace("%20", " ")
    return statement


async def define_api(db):
    if not db['apis']:
        table = db.create_table('apis',
                                primary_id='table',
                                primary_type=db.types.string(25))
        table.create_column('table', db.types.string).create_column('get', db.types.boolean) \
            .create_column('post', db.types.boolean).table.create_column('put', db.types.boolean) \
            .create_column('delete', db.types.boolean)
        db.commit()
        return table
    else:
        return {"configure": "success"}


def init_app(app, sys, access_point="/api", db_type="postgres"):
    # define postgres,mysql as attributes of the object
    db = getattr(sys, db_type)

    @app.get(access_point, tags=[access_point])
    async def api():
        return await define_api(db)

    @app.get(access_point + "/{table}", tags=[access_point])
    async def get(table, request: Request):
        """all elements on a table"""
        if access(db, table, 'get'):
            statement = await url_query(request)
            return await get_list(statement, table)
        else:
            return {"access": "denied"}

    async def get_list(statement, table):
        if statement:
            try:
                return list(db[table].find(text(statement)))
            except Exception as e:
                return "query invalid:" + statement + "-" + e
        else:
            return list(db[table].all())

    @app.post(access_point + "/{table}", tags=[access_point])
    async def post(table, request: Request):
        data = dict(await request.json())
        result = db[table].insert(data)
        return {result: data}

    @app.put(access_point + "/{table}", tags=[access_point])
    async def put(table, request: Request):
        statement = await url_query(request)
        data = dict(await request.json())
        if statement != "":
            result = db[table].update(data, keys=statement.split("=")[0])
        return result

    @app.delete(access_point + "/{table}", tags=[access_point])
    async def delete(table, request: Request):
        statement = await url_query(request)
        if statement != "":
            result = db[table].delete(text(statement))
        return result

    return app
