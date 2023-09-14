from uuid import uuid4

from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from core.settings import templating, redis
from core.models import User
from core.dependencies import is_authenticated

router = APIRouter()


@router.get('/register', name='register')
async def register(request: Request):
    return templating.TemplateResponse(
        name='register.html',
        context={
            'request': request
        }
    )


@router.post(path='/register')
async def register(
        request: Request,
        email: str = Form(),
        password: str = Form()
):
    with User.session() as session:
        user = User(email=email, hashed_password=password)
        session.add(user)
        try:
            session.commit()
        except:
            pass
    return templating.TemplateResponse(
        name='register.html',
        context={
            'request': request
        }
    )


@router.get(path='/login', name='login')
async def login(request: Request):
    return templating.TemplateResponse(
        name='login.html',
        context={
            'request': request
        }
    )


@router.post(path='/login')
async def login(
        request: Request,
        email: str = Form(),
        password: str = Form()
):
    response = templating.TemplateResponse(
        name='login.html',
        context={
            'request': request
        }
    )
    with User.session() as session:
        user = session.query(User).filter_by(email=email).one()
        if user is not None and user.hashed_password == password:
            sessionid = f'{uuid4()}'
            response.set_cookie('sessionid', value=sessionid)
            redis.set(sessionid, user.id)
    return response


@router.get('/logout')
async def logout(request: Request):
    response = RedirectResponse('/login')
    if request.user.is_authenticated:
        redis.delete(request.cookies.get('sessionid'))
        response.delete_cookie('sessionid')
    return response


@router.get('/profile', dependencies=[is_authenticated])
async def profile(request: Request):
    return templating.TemplateResponse(
        name='profile.html',
        context={
            'request': request
        }
    )