"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 16/03/22
@name: routers
"""
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from credits.models.config import CalculatorConfig
from credits.models.user_credit import UserCredits
from credits.schemas.config_schema import CalculatorConfigBase, CalculatorConfigStore
from credits.schemas.user_credit_schema import CreditRequest, CreditUser
from database.settings import API_VERSION
from users.utils import get_current_user
from utils.response import bad_request

router = APIRouter(
    prefix=f'{API_VERSION}credits',
    tags=['credits']
)


@router.get(path='/config/calculator')
def config_calculator():
    config = CalculatorConfig.get_last()
    if not config:
        raise HTTPException(status_code=500, detail='Currently does not exist a config for calculator')
    return CalculatorConfigStore(**jsonable_encoder(config))


@router.post(path='/config/calculator')
def create_config_calculator(config: CalculatorConfigBase, user: Any = Depends(get_current_user)):
    new = CalculatorConfig(**config.dict()).create()
    return CalculatorConfigStore(**config.dict(), id=new.id)


@router.put(path='/config/calculator')
def update_config_calculator(
        config_id: int,
        config: CalculatorConfigBase,
        user: Any = Depends(get_current_user)):
    id = config_id
    data = config.dict().copy()
    if 'id' in data.keys():
        del data['id']
    updated = CalculatorConfig.update(id, data)
    return CalculatorConfigStore(**jsonable_encoder(updated))


########  --- USER CREDIT ENDPOINTS --- #########
@router.post(path='/user/new')
def user_create_credit(credit: CreditRequest, current_user: Any = Depends(get_current_user)):
    """

    :param credit:
    :param current_user:
    :return:
    """

    config = CalculatorConfig.read(credit.credit_config_id)
    if not config:
        raise bad_request(message='Configuration does not exists please contact to admin')
    if credit.amount_credit > config.amount_max:
        raise bad_request(message='Your amount credit is higher that our budget')
    if credit.amount_credit < config.amount_min:
        raise bad_request(message='Your amount credit is smaller that our allow ')

    new_credit = UserCredits(
        **credit.dict(),
        user_id=current_user.id,
        amount_credit_tax=config.amount_tax).create()
    new_credit = jsonable_encoder(new_credit)
    del new_credit['credit_config_id']
    return CreditUser(**jsonable_encoder(new_credit), credit_config_id=jsonable_encoder(config))
