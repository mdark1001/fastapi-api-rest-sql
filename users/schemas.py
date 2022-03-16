"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 15/03/22
@name: schemas
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(
        ...,
        title="User's email",
        example='tangelo@demo.com',
    )
    name: str = Field(
        ...,
        title='Name',
        example='Tangelo',
    )
    last_name: str = Field(
        ...,
        example='Admin',
    )
    phone: str = Field(
        ...,
        example='22112334122'
    )
    is_active: Optional[bool] = Field(
        None,
        title="is this user active?",
    )


class UserLogin(BaseModel):
    email: EmailStr = Field(
        ...,
        example="tangelo@demo.com",
    )
    password: str = Field(
        ...,
        min_length=5,
        example="AwesomePassword"
    )


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=5,
        title="User's password",
        example="AwesomePassword",
    )


class UserRegistered(UserBase):
    user_id: Optional[int]
    token: Optional[str]


class Token(BaseModel):
    token: str
    user: UserBase


class ResetPassword(BaseModel):
    current_password: str = Field(
        ...,
        min_length=5,
        title="User's password",
        example="AwesomePassword",
    )
    new_password: str = Field(
        ...,
        min_length=5,
        title="User's password",
        example="NewAwesomePassword",
    )
