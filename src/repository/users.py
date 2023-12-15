import pickle

from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel



async def get_cache_user_by_email(email: str, cache = None ) -> User | None:
    if email:
        user_bytes = None
        try:
            if cache:
                user_bytes = await cache.get(f"user:{email}")
            if user_bytes is None:
                return None
            user = pickle.loads(user_bytes)  # type: ignore
            print(f"Get from Redis  {str(user.email)}")
        except Exception as err:
            print(f"Error Redis read {err}")
            user = None
        return user


async def update_cache_user(user: User, cache = None):
    if user and cache:
        email = user.email
        try:
            await cache.set(f"user:{email}", pickle.dumps(user))
            await cache.expire(f"user:{email}", 900)
            print(f"Save to Redis {str(user.email)}")
        except Exception as err:
            print(f"Error redis save, {err}")



async def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter_by(email=email).first()


async def create_user(body: UserModel, db: Session):
    g = Gravatar(body.email)

    new_user = User(**body.dict(), avatar=g.get_image())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: UserModel, refresh_token, db: Session):
    user.refresh_token = refresh_token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user