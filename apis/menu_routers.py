from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi import APIRouter, Request

from apis.game_logic.dialogs_builder import ENTRY_DIALOG_NAME


templates = Jinja2Templates(directory='templates')

menu_pages_router = APIRouter()


def start_new_game() -> RedirectResponse:
    """
    Preparatory method to start a new game

    :return: Redirect to a new game
    """
    entry_dialog_id = ENTRY_DIALOG_NAME
    response = RedirectResponse(url=f'/game?d={entry_dialog_id}')
    response.set_cookie(key='dialog', value=entry_dialog_id)
    response.delete_cookie(key='prev_dialog')
    return response


@menu_pages_router.get('/delete_cookies')
def del_cookies():
    """
    Deletes cookies

    :return:
    """
    response = JSONResponse(content={'message': 'session deleted'})
    response.delete_cookie('dialog')
    response.delete_cookie('prev_dialog')
    response.delete_cookie('name')
    return response


@menu_pages_router.get('/', response_class=HTMLResponse)
async def root(request: Request):
    """
    Shows the main menu

    :param request:
    :return:
    """
    return templates.TemplateResponse('general_pages/menu/menu.html', {'request': request})


@menu_pages_router.post('/new_game', response_class=RedirectResponse)
async def new_game():
    """
    Starts a new game, redirects to a new game session

    :return:
    """
    return start_new_game()


@menu_pages_router.post('/continue', response_class=RedirectResponse)
async def continue_game(request: Request):
    """
    Tries to continue a game with a recently saved dialog id

    :param request:
    :return:
    """

    if 'dialog' not in request.cookies:
        return start_new_game()

    dialog_id = request.cookies['dialog']
    response = RedirectResponse(url=f'/game?d={dialog_id}')
    return response


@menu_pages_router.post('/about', response_class=HTMLResponse)
async def about(request: Request):
    """
    Shows the about-page

    :param request:
    :return:
    """
    return templates.TemplateResponse('general_pages/menu/about.html', {'request': request, 'back_url': '/'})
