from ninja import Router
from ninja.errors import HttpError
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from user.schemas.outbound import UserMeOut, SuccessOut, UserRefreshTokenOut
from user.schemas.inbound import UserSignupIn, UserLoginIn, RefreshTokenIn, UserUpdateIn
from user.models import Jwt, User
from user import utils
from django.conf import settings
from api.exceptions import CustomAuthorizationError
from django.http import JsonResponse
from api.security import jwt_auth


User = get_user_model()
router = Router(tags=["Users"])


@router.post(
    "/signup",
    summary="[C] 회원가입",
    description="회원가입을 진행합니다.",
    response={
        200: UserMeOut,
    },
)
async def signup(request, data: UserSignupIn):
    if await User.objects.filter(username=data.username).aexists():
        raise HttpError(420, "이미 등록된 아이디에요.")

    if not await sync_to_async(user.check_password)(data.password):
        raise HttpError(400, "비밀번호가 일치하지 않아요.")

    if not data.terms_of_service:
        raise HttpError(400, "이용약관에 동의해주세요.")

    if not data.privacy_policy_agreement:
        raise HttpError(400, "개인정보 수집 및 이용 동의에 동의해주세요.")

    try:
        user = await sync_to_async(User.objects.create_user)(
            username=data.username,
            password=data.password,
        )

        user = await User.objects.aget(
            id=user.id
        )

        return user
    except Exception as e:
        raise HttpError(
            400, "회원가입 중 오류가 발생했어요. 잠시 후 다시 시도해주세요."
        )


@router.post(
    "/login",
    summary="[C] 로그인",
    description="로그인을 진행합니다.",
    response={
        200: UserMeOut,
    },
)
async def login(request, data: UserLoginIn):

    user = await User.objects.aget(username=data.username)

    if not user:
        raise HttpError(400, "해당 아이디로 등록된 사용자가 없어요.")

    if not await sync_to_async(user.check_password)(data.password):
        raise HttpError(400, "비밀번호가 일치하지 않아요.")

    await Jwt.objects.filter(user_id=user.id).adelete()

    access, access_exp = utils.get_access_token({"user_id": user.id})
    refresh, refresh_exp = utils.get_refresh_token()

    await Jwt.objects.acreate(
        user_id=user.id,
        access=access,
        refresh=refresh,
    )

    response = JsonResponse({"status": user.status})
    if settings.DJANGO_ENV_NAME == "local":
        response = JsonResponse(
            {
                "status": user.status,
                "access_token": access,
                "refresh_token": refresh,
            }
        )

    return utils.set_cookie_jwt(response, access, refresh, access_exp, refresh_exp)


@router.post(
    "/logout",
    summary="[C] 로그아웃",
    description="로그아웃을 진행합니다.",
    response={
        200: SuccessOut,
    },
    auth=jwt_auth,
)
async def logout(request):
    user = request.auth
    await Jwt.objects.filter(user_id=user.id).adelete()
    return {"detail": "로그아웃 되었어요."}


@router.post(
    "/refresh-token",
    summary="[C] 토큰 갱신",
    description="만료된 Access Token을 갱신합니다.",
    response={
        200: UserRefreshTokenOut,
    },
)
async def refresh_token(request, data: RefreshTokenIn):
    try:
        await utils.validate_refresh_token(data.refresh_token)

        # Refresh Token을 통해 DB에서 JWT Entry를 가져옴
        jwt_entry = await Jwt.objects.select_related("user").aget(
            refresh=data.refresh_token
        )

        user = jwt_entry.user
        if not user:
            raise HttpError(400, "Invalid user")

        # 새로운 Access Token 및 Refresh Token 생성
        access, access_exp = utils.get_access_token({"user_id": user.id})
        refresh, refresh_exp = utils.get_refresh_token()

        # 기존 Refresh Token 업데이트
        await Jwt.objects.aupdate_or_create(
            user_id=user.id,
            defaults={"access": access, "refresh": refresh},
        )

        response = JsonResponse({"status": user.status})
        if settings.DJANGO_ENV_NAME == "local":
            response = JsonResponse(
                {
                    "status": user.status,
                    "access_token": access,
                    "refresh_token": refresh,
                }
            )
        return utils.set_cookie_jwt(response, access, refresh, access_exp, refresh_exp)

    except CustomAuthorizationError as e:
        raise HttpError(400, str(e))


@router.get(
    "/me",
    summary="[C] 내 정보 조회",
    description="내 정보를 조회합니다.",
    response={200: UserMeOut},
    auth=jwt_auth,
)
async def get_me(request):
    user = await User.objects.select_related("region", "district__region").aget(
        id=request.auth.id
    )
    return user


@router.patch(
    "/{user_id}",
    summary="[C] 회원 정보 수정",
    description="회원 정보를 수정합니다.",
    response={200: UserMeOut},
    auth=jwt_auth,
)
async def update_user(request, user_id: int, data: UserUpdateIn):
    async def get_user_by_id(user_id: int):
        return await User.objects.aget(
            id=user_id
        )

    if request.auth.status != User.UserStatusChoice.admin:
        raise HttpError(400, "관리자가 아니에요.")

    user = await get_user_by_id(user_id)

    await user.asave()
    return await get_user_by_id(user_id)
