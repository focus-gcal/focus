from users.auth.ninja_auth import JWTAuth

from .api import router


@router.get("me", auth=JWTAuth())
def me(request):
    return {
        "id": request.auth.id,
        "username": request.auth.username,
        "email": request.auth.email,
    }
