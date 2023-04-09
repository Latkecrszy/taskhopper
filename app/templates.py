from app.constants import *
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import Response, JSONResponse, RedirectResponse

templates = Jinja2Templates(directory='templates')

async def main(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse('main.html',
                                     {'request': request})


async def not_found(request: Request, exc) -> Response:
    return templates.TemplateResponse('404.html', {'request': request}, status_code=exc.status_code)


async def dashboard(request: Request) -> Response:
    username = request.cookies.get('username')
    user = db.login.find_one({'username': username})
    view = user.get('view') if user.get('view') else 'work'
    print(view)
    return templates.TemplateResponse('dashboard.html', {'request': request, 'username': username, 'view': view})
