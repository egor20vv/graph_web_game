import os

import uvicorn

from fastapi import FastAPI


from apis.game_router import game_pages_router
from apis.menu_routers import menu_pages_router


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


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


if __name__ == '__main__':
    list_files(str(__file__).replace('\\main.py', ''))
