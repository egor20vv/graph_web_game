from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request, Form

from .game_logic.dialogs_builder import get_built_dialogs

templates = Jinja2Templates(directory='templates/')

game_pages_router = APIRouter()

game_dialogs = get_built_dialogs()


@game_pages_router.post('/game', response_class=HTMLResponse)
def game(request: Request, d: str):
    """
    Response html page with dialog

    :param request:
    :param d: dialog
    :return:
    """

    current_dialog = game_dialogs[d]

    response_arguments = {'request': request,
                          'header': current_dialog.header,
                          'content': current_dialog.content,
                          'choices': current_dialog.choices,
                          'back_url': {'url': '/', 'button_content': 'Я наигрался'}}

    if 'prev_dialog' in request.cookies:
        response_arguments['back_dialog'] = request.cookies['prev_dialog']

    response = templates.TemplateResponse('general_pages/game/game.html', response_arguments)

    return response


@game_pages_router.post('/response', response_class=RedirectResponse)
def choice_dialog(request: Request, ch: str = Form(...)):
    """
    (Calls from a form) Redirects to /game with chosen dialog id (?d=<chosen_dialog_id>)

    :param request:
    :param ch: chosen dialog id
    :return:
    """
    response = RedirectResponse(f'/game?d={ch}')

    response.set_cookie(key='prev_dialog', value=request.cookies['dialog'])
    response.set_cookie(key='dialog', value=ch)

    return response


@game_pages_router.post('/back', response_class=RedirectResponse)
def back_to_prev_dialog(request: Request, ch: str = Form(...)):
    """
    (Calls from a form) Redirects to the /game with a previous dialog id

    :param request:
    :param ch: previously chosen dialog id
    :return:
    """
    response = RedirectResponse(f'/game?d={ch}')
    if 'prev_dialog' in request.cookies:
        response.delete_cookie(key='prev_dialog')
        response.set_cookie(key='dialog', value=ch)
    return response


@game_pages_router.get('/game', response_class=HTMLResponse)
async def try_to_cheat(request: Request, d: str):
    """
    Generates a funny page that says "don't cheat" if user tries to manually enter a dialog id to get it

    :param request:
    :param d: dialog id
    :return:
    """
    return templates.TemplateResponse('general_pages/game/dont_like_cheaters.html', {'request': request})
