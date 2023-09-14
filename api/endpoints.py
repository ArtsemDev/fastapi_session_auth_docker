from .router import router
from core.tasks import ping


@router.get(path='/')
async def index():
    ping.delay()
    return {'status': 'OK'}
