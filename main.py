from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

from api.endpoints import router as api_router
from auth.views import router as auth_router
from core.middleware import MIDDLEWARES


app = FastAPI()
app.include_router(router=api_router)
app.include_router(router=auth_router)


@app.exception_handler(401)
async def unauthorized_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse('/login')


for middleware, options in MIDDLEWARES:
    app.add_middleware(middleware, **options)
