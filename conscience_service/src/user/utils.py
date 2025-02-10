import jwt, random, string
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from api.exceptions import CustomAuthorizationError
from zoneinfo import ZoneInfo


User = get_user_model()


def get_random(length):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_access_token(payload):
    exp = timezone.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_TIME)
    return (
        jwt.encode(
            {
                "exp": exp,
                **payload,
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        ),
        exp,
    )


def get_refresh_token():
    exp = timezone.now() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRATION_TIME)
    return (
        jwt.encode(
            {
                "exp": exp,
                "data": get_random(10),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        ),
        exp,
    )


async def validate_refresh_token(token):
    try:
        decoded = jwt.decode(token, key=settings.SECRET_KEY, algorithms="HS256")
        naive_datetime = datetime.fromtimestamp(decoded["exp"])
        exp_datetime = timezone.make_aware(naive_datetime, ZoneInfo("UTC"))
        if exp_datetime < timezone.now():
            raise CustomAuthorizationError("토큰이 만료되었습니다.", 401)
    except jwt.ExpiredSignatureError:
        raise CustomAuthorizationError("토큰이 만료되었습니다.", 401)
    except jwt.DecodeError:
        raise CustomAuthorizationError("올바르지 않은 토큰입니다.", 401)


async def decodeJWT(bearer):
    if not bearer:
        return None

    token = bearer[7:]
    try:
        decoded = jwt.decode(token, key=settings.SECRET_KEY, algorithms="HS256")
        naive_datetime = datetime.fromtimestamp(decoded["exp"])
        exp_datetime = timezone.make_aware(naive_datetime, ZoneInfo("UTC"))
        if exp_datetime < timezone.now():
            raise CustomAuthorizationError("토큰이 만료되었습니다.", 401)
    except jwt.exceptions.ExpiredSignatureError:
        raise CustomAuthorizationError("토큰이 만료되었습니다.", 401)
    except jwt.exceptions.DecodeError:
        raise CustomAuthorizationError("올바르지 않은 토큰입니다.", 401)

    if decoded:
        try:
            return await User.objects.aget(id=decoded["user_id"])
        except User.DoesNotExist:
            return None


# async def create_password_reset_token(user):
#     token = secrets.token_urlsafe(32)
#     await PasswordEmailVerification.objects.filter(
#         user=user, is_verified=False
#     ).adelete()
#     verification = await PasswordEmailVerification.objects.acreate(
#         user=user, token=token, is_verified=False
#     )
#     return verification


def set_cookie_jwt(response, access, refresh, access_exp, refresh_exp, reset=None):
    domain = settings.SESSION_COOKIE_DOMAIN
    secure = settings.SESSION_COOKIE_SECURE
    samesite = settings.SESSION_COOKIE_SAMESITE

    response.set_cookie(
        key="access",
        value=access,
        expires=access_exp,
        secure=secure,
        samesite=samesite,
        httponly=False,
        domain=domain,
    )

    response.set_cookie(
        key="refresh",
        value=refresh,
        expires=refresh_exp,
        secure=secure,
        samesite=samesite,
        httponly=True,
        domain=domain,
    )

    if reset:
        response.set_cookie(
            key="reset",
            value=reset,
            expires=access_exp,
            secure=secure,
            samesite=samesite,
            httponly=True,
            domain=domain,
        )

    return response
