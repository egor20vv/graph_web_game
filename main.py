from typing import List

import uvicorn

from fastapi import FastAPI, Form  # , Request
from fastapi.responses import Response, HTMLResponse, RedirectResponse, JSONResponse
# from jinja2 import Template
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

import dialogs

import re
import os


app = FastAPI()

templates = Jinja2Templates(directory='templates')

game_dialogs = dialogs.get_built_dialogs()


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/new_game', response_class=RedirectResponse)
async def new_game():
    entry_dialog_id = dialogs.ENTRY_DIALOG_NAME
    response = RedirectResponse(url=f'/game?d={entry_dialog_id}')
    response.set_cookie(key='dialog', value=entry_dialog_id)
    return response


@app.post('/continue', response_class=RedirectResponse)
async def continue_game(request: Request):
    if 'dialog' not in request.cookies:
        entry_dialog_id = dialogs.ENTRY_DIALOG_NAME
        response = RedirectResponse(url=f'/game?d={entry_dialog_id}')
        response.set_cookie(key='dialog', value=entry_dialog_id)
        return response

    dialog_id = request.cookies['dialog']
    response = RedirectResponse(url=f'/game?d={dialog_id}')
    return response


@app.post('/about')
async def about():
    return {'info': 'here is some info'}


@app.post('/game', response_class=HTMLResponse)
async def game(request: Request, d: str):
    if dialogs.ENTRY_DIALOG_NAME == request.cookies['dialog']:
        pass
    else:
        pass

    current_dialog = game_dialogs[d]

    response = templates.TemplateResponse('game.html', {'request': request,
                                                        'header': current_dialog.header,
                                                        'content': current_dialog.content,
                                                        'choices': current_dialog.choices})
    return response


@app.post('/response', response_class=RedirectResponse)
def choice_receiver(ch: str = Form(...)):
    response = RedirectResponse(f'/game?d={ch}')
    response.set_cookie(key='dialog', value=ch)

    return response


@app.get('/game')
async def try_to_cheat(request: Request, d: str):
    return {'message': 'Мы читеров не любим!!!'}


if __name__ == '__main__':
    name = re.search(r'[/\\](?P<name>[\w]+).(?P<extansion>[\w]+)$', __file__).group(1)
    port = os.environ['PORT'] if 'PORT' in os.environ else 5000

    uvicorn.run(f"{name}:app", port=port, reload=True, access_log=False)
