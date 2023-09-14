from fastapi import Depends, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from typing_extensions import Annotated


def _is_authenticated(request: Request):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


is_authenticated = Depends(_is_authenticated)
