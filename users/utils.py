"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 15/03/22
@name: utils
"""
import logging
from datetime import timedelta, datetime
from typing import Union, Any

import jwt
from fastapi import Header, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import settings
from database.depends import get_db
from users.models import User
from utils.response import bad_request

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"

logger = logging.getLogger(__name__)


def encrypt(password: str) -> str:
    """
    Encrypt a string
    :param password:
    :return:
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """

    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
        subject: Union[str, Any],
        expires_delta: timedelta = None
) -> str:
    """
    Create User token
    :param subject:
    :param expires_delta:
    :return:
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.ACCESS_TOKEN_EXPIRE_DAYS
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token


def get_current_user(token: str = Header(...), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception) as e:
        logger.error(e)
        raise bad_request('Token is invalid or expired')
    user = db.query(User).filter(User.id == payload.get('sub', 0)).first()
    if not user:
        logger.error("User does not exits %s" % payload.get('sub'))
        raise bad_request('The token does not belong to any user')
    return user
