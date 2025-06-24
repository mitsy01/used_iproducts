from typing import Annotated, Optional

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.users.models import User
from app.db.base import get_db
from app.config import settings


def decode_jwt(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/urers/token/"))]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(payload=payload, key=settings.secret_key, algorithm=[settings.algorithm])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    return username
    
    
async def get_user(username: str, db: AsyncSession) -> Optional[User]:
    query = select(User).filter_by(username=username)
    result = await db.execute(query)
    return result.scalar_one_or_none()
    

async def sign_up(username:str, password:str, db: AsyncSession):
    user = await get_user(username=username, db=db)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такий користувач вже існує.")
    
    user = User(username=username, password=password)
    db.add(user)
    await db.commit()
    

async def sign_in(username: str, password: str, db: AsyncSession) -> str:
    user = await get_user(username=username, db=db)
    if not user or user.verify_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Логін або пароль не правильний.")
    return user.create_token()