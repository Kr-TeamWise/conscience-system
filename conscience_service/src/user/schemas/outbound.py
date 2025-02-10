from ninja import Schema, ModelSchema
from user.models import User


class UserMeOut(Schema):
    username: str
    status: str

class UserLoginOut(Schema):
    access_token: str
    refresh_token: str
    status: str


class UserRefreshTokenOut(Schema):
    access_token: str
    refresh_token: str


class SuccessOut(Schema):
    detail: str
