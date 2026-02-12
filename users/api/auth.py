from ninja import Router, Schema
from django.contrib.auth import get_user_model

User = get_user_model()
router = Router()


class RegisterIn(Schema):
    username: str
    email: str
    password: str
    max_duration_chunk:int | None = None

class RegisterOut(Schema):
    ok: bool
    id : int | None = None
    username : str | None = None
    email : str | None = None
    error: str | None = None



@router.post("/register", response=RegisterOut)
def register(request, data: RegisterIn):
    username = data.username.strip()
    email = data.email.strip().lower()
    
    if User.objects.filter(username=username).exists():
        return RegisterOut(ok=False, error="Username already exists.")
    if User.objects.filter(email=email).exists():
        return RegisterOut(ok=False, error="Email already exists.")
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=data.password,
    )
    if data.max_duration_chunk is not None:
        user.max_duration_chunk = data.max_duration_chunk
        user.save(update_fields=["max_duration_chunk"])
    return RegisterOut(ok=True, id=user.id, username=user.username, email=user.email)