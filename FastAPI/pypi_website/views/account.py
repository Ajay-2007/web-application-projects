import fastapi

from fastapi_chameleon import template
from starlette.requests import Request

from viewmodels.account.account_viewmodel import AccountViewModel
from viewmodels.account.login_viewmodel import LoginViewModel
from viewmodels.account.register_viewmodel import RegisterViewModel

router = fastapi.APIRouter()


@router.get('/account')
def index(request: Request):
    vm = AccountViewModel(request)
    return {}


@router.get('/account/register')
def index(request: Request):
    vm = RegisterViewModel(request)
    return {}


@router.get('/account/login')
def index(request: Request):
    vm = LoginViewModel(request)
    return {}


@router.get('/account/logout')
def index(request: Request):
    vm = RegisterViewModel(request)
    return {}
