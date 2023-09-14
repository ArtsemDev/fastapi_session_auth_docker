import typing

from starlette.authentication import AuthenticationBackend, AuthCredentials
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection

from core.models import User
from core.settings import redis


class SessionAuthenticationBackend(AuthenticationBackend):

    async def authenticate(
        self, conn: HTTPConnection
    ) -> typing.Optional[typing.Tuple["AuthCredentials", User]]:
        auth = conn.cookies.get('sessionid', None)
        if auth is None:
            return

        user_id = redis.get(auth)
        if user_id is None:
            return

        user_id = int(user_id.decode())
        with User.session() as session:
            user = session.get(User, user_id)
            if user is None:
                return

        return AuthCredentials(['authenticated']), user


MIDDLEWARES = (
    (AuthenticationMiddleware, {'backend': SessionAuthenticationBackend()}),
)
