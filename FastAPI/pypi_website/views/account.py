import fastapi

from fastapi_chameleon import template

router = fastapi.APIRouter()


@router.get('/account')
def index():
    return {}


@router.get('/account/register')
def index():
    return {}


@router.get('/account/login')
def index():
    return {}


@router.get('/account/logout')
def index():
    return {}
