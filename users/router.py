"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 15/03/22
@name: router
"""
from typing import Any

from fastapi import APIRouter, Depends, status, Header
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from database.depends import get_db
from users.models import User
from users.schemas import UserLogin, UserBase, UserCreate, UserRegistered, ResetPassword
from users.utils import encrypt, create_access_token, verify_password
from users.utils import get_current_user
from utils.response import not_found, bad_request, success_request

router = APIRouter(
    prefix='/account',
    tags=['account']
)


@router.post(
    path='/login',
    response_model=UserRegistered,
)
def login(userlogin: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == userlogin.email and
        User.is_active
    ).first()
    if not user:
        raise not_found("Email or password are incorrect")
    if not user.is_active:
        raise bad_request('This user is inactive, please contact us to help you.')
    if not verify_password(userlogin.password, user.password):
        raise not_found("Email or password are incorrect")
    user = UserRegistered(
        **jsonable_encoder(user),
        user_id=user.id,
        token=create_access_token(user.id)
    )
    return user


@router.post(
    path='/register',
    response_model=UserRegistered,
    status_code=status.HTTP_201_CREATED,
)
def register(user: UserCreate, db: Session = Depends(get_db)):
    exists_users = db.query(User).filter(User.email == user.email).count()
    if exists_users:
        raise bad_request('Already exists an user with this email: %s' % user.email)
    user.password = encrypt(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    user = UserRegistered(**user.dict(), user_id=new_user.id, token=create_access_token(new_user.id))
    return user


@router.get(
    path='/verify',
)
def verify_token(current_user: Any = Depends(get_current_user)):
    return success_request('This token is right')


@router.put(
    path='/reset-password',
    response_model=UserRegistered,
)
def reset_password(password: ResetPassword, current_user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    if not verify_password(password.current_password, current_user.password):
        raise bad_request('Password is wrong')
    if password.current_password == password.new_password:
        raise bad_request('Current password is equals to new password')
    current_user.password = encrypt(password.new_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return success_request('Password has beem updated')


@router.get(
    path='/user/{user_id}',
)
def get_user_id(user_id: int, current_user: Any = Depends(get_current_user)):
    user = jsonable_encoder(User.read(user_id))
    return UserBase(**user)


@router.delete(path='/user/{user_id}')
def delete_user(user_id: int, current_user: Any = Depends(get_current_user)):
    try:
        User.unlink(user_id)
    except Exception as e:
        return bad_request(str(e))
    return success_request(message="User has been deleted ")
