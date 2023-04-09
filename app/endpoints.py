from app.constants import *
from starlette.requests import Request
from starlette.responses import Response, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse
import random, string
import urllib


def gen_token() -> str:
    session = ''.join(random.choices([*string.ascii_letters, *(str(i) for i in range(10))], k=30))
    while db.sessions.find_one({'session_id': session}) is not None:
        session = ''.join(random.choices([*string.ascii_letters, *(str(i) for i in range(10))], k=30))
    return session


async def signup(request: Request) -> JSONResponse:
    data = await request.json()
    token = gen_token()
    db.tokens.insert_one({'username': data.get('username').lower(), 'token': token})
    print(data.get('dob'))
    age = 2023-int(data.get('dob').split('-')[-1])
    print(age)
    if db.login.find_one({'username': data.get('username').lower()}):
        return JSONResponse({'error': 'email in use'}) 

    db.login.insert_one({
        'username': data.get('username').lower(), 'password': data.get('password'), 'name': data.get('name'), 
        'address': data.get('address').lower(), 'dob': data.get('dob'), 'age': age, 'city': data.get('city').lower(), 
        'state': data.get('state'), 'zip': data.get('zip')
    })
    return JSONResponse({'token': token, 'username': data.get('username').lower(), 'error': ''})



async def login(request: Request) -> JSONResponse:
    data = await request.json()
    token = gen_token()
    db.tokens.insert_one({'username': data.get('username').lower(), 'token': token})
    print(data.get('username').lower())
    print(data.get('password'))
    if not db.login.find_one({'username': data.get('username').lower(), 'password': data.get('password')}):
        return JSONResponse({'error': 'password incorrect'})
    
    return JSONResponse({'token': token, 'username': data.get('username').lower(), 'error': ''})



async def set_cookie(request: Request) -> Response:
    username = request.query_params.get('username').lower()
    if not db.tokens.find_one({'username': username, 'token': request.query_params.get('token')}):
        return RedirectResponse('/')
    db.tokens.find_one_and_delete({'username': username, 'token': request.query_params.get('token')})
    response = RedirectResponse('/dashboard')
    response.set_cookie('username', username)
    session_id = gen_token()
    db.sessions.insert_one({'username': username, 'session_id': session_id})
    response.set_cookie('session_id', session_id, max_age=3153600000)
    return response

    


async def create_job(request: Request) -> JSONResponse:
    # Arguments to take: payment, name, category, location, ...
    data = request.json()
    id = int(db.id.find_one_and_update({'_id': 'id'}, {'$inc': {'id': 1}}))
    db.jobs.insert_one({'price': data.get('price'), 'username': data.get('username').lower(),
                    'location': data.get('location'), 'name': data.get('name'), 'category': data.get('category'), 'id': id})
    
    return JSONResponse({'error': '', 'message': 'success'}, 200)


async def accept_job(request: Request) -> JSONResponse:
    data = request.json()
    job = db.active_jobs.insert_one(db.jobs.find_one_and_delete({'id': data.get('id')}))
    user = db.login.find_one({'username': data.get('username').lower()})
    message = twilio.messages.create(
        from_='+18339952479',
        body=f'You just accepted the job {data.get("name")} for {job.get("username").lower()} for ${job.get("price")}.',
        to=user.get('number')
    )

    message = twilio.messages.create(
        from_='+18339952479',
        body=f'You just accepted the job {data.get("name")} for {job.get("username").lower()} for ${job.get("price")}.',
        to=user.get('number')
    )
    print(message.sid)
    return JSONResponse({'error': '', 'message': 'success'}, 200)


async def switch_view(request: Request) -> JSONResponse:
    data = await request.json()
    user = db.login.find_one({'username': data.get('username').lower()})
    if user.get('view') == 'pay':
        db.login.find_one_and_update({'username': data.get('username').lower()}, {'$set': {'view': 'work'}})
    else:
        db.login.find_one_and_update({'username': data.get('username').lower()}, {'$set': {'view': 'pay'}})
    return JSONResponse({'error': '', 'message': 'success'}, 200)


async def encode(request: Request) -> JSONResponse:
    data = await request.json()
    return JSONResponse({'address': urllib.parse.quote(data.get('address').encode())})
