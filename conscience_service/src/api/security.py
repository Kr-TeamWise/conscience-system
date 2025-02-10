import jwt
from typing import Any, Optional
from django.http import HttpRequest
from ninja.security import HttpBearer
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone


User = get_user_model()


class JWTAuth(HttpBearer):
    async def __call__(self, request: HttpRequest) -> Optional[Any]:
        headers = request.headers
        auth_value = headers.get(self.header)

        if not auth_value:
            token = request.COOKIES.get("access")
            if token:
                return await self.authenticate(request, token)
            return None

        parts = auth_value.split(" ")
        if parts[0].lower() != self.openapi_scheme:
            return None

        token = " ".join(parts[1:])
        return await self.authenticate(request, token)

    async def authenticate(self, request, token):
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if decoded["exp"] < timezone.now().timestamp():
                return None  # 토큰이 만료되었습니다.

            user_id = decoded.get("user_id")
            if user_id:
                # return await User.objects.aget(id=user_id)
                return await User.objects.aget(id=user_id)
        except jwt.ExpiredSignatureError:
            return None  # 토큰 만료 에러 처리
        except jwt.DecodeError:
            return None  # 디코드 에러 처리
        except User.DoesNotExist:
            return None  # 사용자가 존재하지 않는 경우
        return None


jwt_auth = JWTAuth()
