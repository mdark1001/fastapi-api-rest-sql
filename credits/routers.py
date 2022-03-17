"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 16/03/22
@name: routers
"""
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder

from credits.models import CalculatorConfig
from credits.schemas import CalculatorConfigBase, CalculatorConfigStore
from users.utils import get_current_user

router = APIRouter(
    prefix='/credits',
    tags=['credits']
)


@router.get(path='/config/calculator')
def config_calculator():
    config = CalculatorConfig.get_last()
    if not config:
        raise HTTPException(status_code=500, detail='Currently does not exist a config for calculator')
    return CalculatorConfigBase(**jsonable_encoder(config))


@router.post(path='/config/calculator')
def create_config_calculator(config: CalculatorConfigBase, user: Any = Depends(get_current_user)):
    new = CalculatorConfig(**config.dict()).create()
    return CalculatorConfigStore(**config.dict(), id=new.id)
