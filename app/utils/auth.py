import asyncio
from datetime import datetime, timedelta, timezone
import jwt
from app.config import settings

async def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"iat": now, "exp": expire})

    loop = asyncio.get_running_loop()
    token = await loop.run_in_executor(
        None,
        lambda: jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    )
    return token

async def decode_access_token(token: str) -> dict:
    loop = asyncio.get_running_loop()
    try:
        decoded = await loop.run_in_executor(
            None,
            lambda: jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        )
        return decoded
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

