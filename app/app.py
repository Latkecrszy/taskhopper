from starlette.applications import Starlette
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles
from app.constants import *
from app.endpoints import *
from app.templates import *


routes = [
    Route('/', endpoint=main, methods=['GET']),
    Route('/signup', endpoint=signup, methods=['POST']),
    Route('/login', endpoint=login, methods=['POST']),
    Route('/set_cookie', endpoint=set_cookie, methods=['GET']),
    Route('/dashboard', endpoint=dashboard, methods=['GET']),
    Route('/encode', endpoint=encode, methods=['POST']),
    Route('/switch-view', endpoint=switch_view, methods=['POST']),
    Mount('/static', StaticFiles(directory='static'), name='main.css'),
    Mount('/static', StaticFiles(directory='static'), name='globals.css'),
    Mount('/static', StaticFiles(directory='static'), name='main.js'),
    Mount('/static', StaticFiles(directory='static'), name='globals.js'),
    Mount('/static/images', StaticFiles(directory='static'), name='grasshopper.svg'),
    Mount('/static/images', StaticFiles(directory='static'), name='homepage-photo.jpg')
]


app = Starlette(routes=routes, debug=False, exception_handlers={404: not_found}, on_startup=[lambda: print('Started app.')])
