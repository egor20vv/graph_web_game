import uvicorn

from fastapi import FastAPI

from apis.game_router import game_pages_router
from apis.menu_routers import menu_pages_router

import os


def include_routers(_app):
    _app.include_router(menu_pages_router)
    _app.include_router(game_pages_router)


def set_app():
    _app = FastAPI()
    include_routers(_app)
    return _app


# def start_uvicorn(file_name: str, app_name: str):
#     port = os.environ['PORT'] if 'PORT' in os.environ else 5000
#     uvicorn.run(f"{file_name}:{app_name}", port=port, reload=True, access_log=False)


app = set_app()


if __name__ == '__main__':
    pass
    #start_uvicorn('main', 'app')
