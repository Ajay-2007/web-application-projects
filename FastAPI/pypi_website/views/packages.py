import fastapi

from fastapi_chameleon import template
from starlette.requests import Request

from viewmodels.home.indexviewmodel import IndexViewModel
from viewmodels.packages.details_viewmodel import DetailsViewModel
from viewmodels.shared.viewmodel import ViewModelBase

router = fastapi.APIRouter()


@router.get('/project/{package_name}')
@template(template_file='packages/details.pt')
async def details(package_name: str, request: Request):
    vm = DetailsViewModel(package_name, request)
    await vm.load()

    return vm.to_dict()
