import asyncio
from datetime import datetime, timedelta, timezone
import jwt
from app.config import settings

async def create_decode_token(
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