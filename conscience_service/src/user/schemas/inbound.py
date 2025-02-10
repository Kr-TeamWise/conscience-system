from ninja import Schema
from user.models import User


class UserSignupIn(Schema):
    username: str
    password: str
    password_confirm: str


class UserUpdateIn(Schema):
    real_name: str
    phone: str
    memo: str


class UserLoginIn(Schema):
    username: str
    password: str


class RefreshTokenIn(Schema):
    refresh_token: str
