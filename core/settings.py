from pydantic import PostgresDsn, RedisDsn, Field
from pydantic_settings import BaseSettings
from celery import Celery
from redis import Redis
from starlette.templating import Jinja2Templates


class Settings(BaseSettings):
    DB_URL: PostgresDsn
    CELERY_RESULT_BACKEND: RedisDsn
    CELERY_BROKER_URL: RedisDsn
    CELERY_RESULT_EXPIRES: int
    REDIS_URL: RedisDsn = Field(default='redis://redis:6379/2')


settings = Settings()
celery = Celery()
celery.config_from_object(obj=settings, namespace='CELERY')
celery.autodiscover_tasks(packages=['core'])
redis = Redis.from_url(url=settings.REDIS_URL.unicode_string())
templating = Jinja2Templates(directory='templates')