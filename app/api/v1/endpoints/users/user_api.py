from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.db.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Fetch user by primary key ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Fetch user by unique email address."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """Create a new user with hashed password."""
    # Ensure password length stays within safe limits before passing to hash function
    safe_password = user_in.password[:72]
    print("==========================")
    print(safe_password)
    print("==========================")
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(safe_password),
        full_name=user_in.full_name,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    """Verify credentials and return user object if valid."""
    user = await get_user_by_email(db, email)
    if not user:
        return None
    
    safe_password = password[:72]
    if not verify_password(safe_password, user.hashed_password):
        return None
        
    return user