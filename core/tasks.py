from .settings import celery


@celery.task()
def ping():
    with open('out.txt', 'a', encoding='utf-8') as file:
        file.write('hello from docker compose \n')
