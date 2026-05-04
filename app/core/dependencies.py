import jwt
from fastapi import Request, HTTPException, status

from app.core.config import settings

PUBLIC_ROUTES: set[tuple[str, str]] = {
    ("POST", "/usuarios/login"),
    ("POST", "/usuarios/register"),
}


async def get_current_user(request: Request) -> dict:
    path = request.url.path
    method = request.method.upper()

    for pub_method, pub_path in PUBLIC_ROUTES:
        if method == pub_method and path.startswith(pub_path):
            return {}

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.removeprefix("Bearer ")

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_aud": False},
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {exc}")

    return payload


def extract_role(payload: dict) -> str:
    role = (
        payload.get("user_metadata", {}).get("role")
        or payload.get("app_metadata", {}).get("role")
        or payload.get("role")
        or "user"
    )
    return str(role)
