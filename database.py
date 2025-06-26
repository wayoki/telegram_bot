import boto3
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, selectinload
from sqlalchemy.future import select
from sqlalchemy.sql.expression import func, and_
from config_reader import config
from dictionary import texts

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    gender_wf = Column(String, nullable=False)
    introduction = Column(String, nullable=True)
    language = Column(String, nullable=False)
    views = relationship(
        "UserView",
        back_populates="user",
        foreign_keys="[UserView.user_id]",
        lazy="selectin"
    )
    likes = relationship(
        "UserLike",
        back_populates="user",
        foreign_keys="[UserLike.user_id]",
        lazy="selectin"
    )
    was_liked = relationship(
        "UserWasLiked",
        back_populates="user",
        foreign_keys="[UserWasLiked.user_id]",
        lazy="selectin"
    )
    matches_user_1 = relationship(
        "UserMatch",
        back_populates="user_1",
        foreign_keys="[UserMatch.user_1_id]",
        lazy="selectin"
    )
    matches_user_2 = relationship(
        "UserMatch",
        back_populates="user_2",
        foreign_keys="[UserMatch.user_2_id]",
        lazy="selectin"
    )

class UserView(Base):
    __tablename__ = 'user_views'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    viewed_user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    user = relationship("User", back_populates="views", foreign_keys=[user_id])
    viewed_user = relationship("User", foreign_keys=[viewed_user_id])
    __table_args__ = (UniqueConstraint('user_id', 'viewed_user_id', name='_user_view_uc'),)

class UserLike(Base):
    __tablename__ = 'user_likes'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    liked_user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    user = relationship("User", back_populates="likes", foreign_keys=[user_id])
    liked_user = relationship("User", foreign_keys=[liked_user_id])
    __table_args__ = (UniqueConstraint('user_id', 'liked_user_id', name='_user_like_uc'),)

class UserWasLiked(Base):
    __tablename__ = 'was_liked'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    liked_user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    user = relationship("User", foreign_keys=[user_id], lazy="selectin")
    liked_user = relationship("User", foreign_keys=[liked_user_id], lazy="selectin")
    __table_args__ = (UniqueConstraint('user_id', 'liked_user_id', name='_was_liked_uc'),)

class UserMatch(Base):
    __tablename__ = 'user_matches'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_1_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    user_2_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    user_1 = relationship("User", foreign_keys=[user_1_id])
    user_2 = relationship("User", foreign_keys=[user_2_id])
    __table_args__ = (UniqueConstraint('user_1_id', 'user_2_id', name='_user_match_uc'),)

s3_client = boto3.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=config.S3_ACCESS_KEY,
    aws_secret_access_key=config.S3_SECRET_KEY,
)

BUCKET_NAME = config.BUCKET_NAME

DATABASE_URL = f"postgresql+asyncpg://{config.POSTGRES_USER.get_secret_value()}:{config.POSTGRES_PASSWORD.get_secret_value()}@{config.POSTGRES_HOST}/{config.POSTGRES_NAME}"
engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

async def save_user_data(user_data):
    async for session in get_session():
        query = select(User).filter(User.user_id == user_data['user_id'])
        result = await session.execute(query)
        existing_user = result.scalars().first()
        if existing_user:
            return "User already exists"
        new_user = User(
            user_id=user_data['user_id'],
            name=user_data['name'],
            age=user_data['age'],
            gender=user_data['gender'],
            gender_wf=user_data['gender_wf'],
            introduction=user_data['introduction'],
            language=user_data['language']
        )
        session.add(new_user)
        await session.commit()

async def get_user_data(user_id: int):
    async for session in get_session():
        query = select(User).filter(User.user_id == user_id)
        result = await session.execute(query)
        user = result.scalars().first()
        return user

async def show_user_data(user_data):
    user = await get_user_data(user_data['user_id'])
    lang_texts = texts.get(user.language, texts['English'])
    profile = lang_texts["your_profile"].format(
        user.name,
        user.age,
        user.gender,
        user.gender_wf,
        user.introduction
    )
    return profile

async def delete_user_data(user_id: int):
    async for session in get_session():
        query = select(User).filter(User.user_id == user_id)
        result = await session.execute(query)
        user = result.scalars().first()
        await session.delete(user)
        await session.commit()

async def update_user_data(user_id: int, name: str = None, age: int = None, gender: str = None, gender_wf: str = None, introduction: str = None, language: str = None):
    async for session in get_session():
        query = select(User).filter(User.user_id == user_id)
        result = await session.execute(query)
        user = result.scalars().first()
        if name:
            user.name = name
        if age is not None:
            user.age = age
        if gender:
            user.gender = gender
        if gender_wf:
            user.gender_wf = gender_wf
        if introduction:
            user.introduction = introduction
        if language:
            user.language = language
        await session.commit()

async def upload_media(bot, file_path: str, file_name: str, user_id: str, media_type: str):
    file = await bot.download_file(file_path)
    match media_type:
        case "photo":
            file_name = f"{file_name}.jpg"
            content_type = "image/jpeg"
        case "video":
            file_name = f"{file_name}.mp4"
            content_type = "video/mp4"
        case _:
            return None
    file_path = f"users/{user_id}/{file_name}"
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=file_path,
        Body=file,
        ContentType=content_type
    )
    file_url = f"https://{BUCKET_NAME}.s3.yandexcloud.net/{file_path}"
    return file_url

async def get_next_user(db_session: AsyncSession, user_id: int):
    result = await db_session.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return None
    result = await db_session.execute(
        select(User)
        .options(selectinload(User.views))
        .where(
            and_(
                User.user_id != user_id,
                ~User.user_id.in_(select(UserView.viewed_user_id).where(UserView.user_id == user_id))
            )
        )
        .order_by(func.random())
    )
    next_user = result.scalars().first()
    return next_user

async def add_viewed_user(db_session: AsyncSession, user_id: int, viewed_user_id: int):
    existing_view = await db_session.execute(
        select(UserView).filter_by(user_id=user_id, viewed_user_id=viewed_user_id)
    )
    existing_view = existing_view.scalar_one_or_none()
    if not existing_view:
        viewed_user = UserView(user_id=user_id, viewed_user_id=viewed_user_id)
        db_session.add(viewed_user)
        await db_session.commit()

async def add_liked_user(db_session: AsyncSession, user_id: int, liked_user_id: int):
    existing_like = await db_session.execute(
        select(UserLike).filter_by(user_id=user_id, liked_user_id=liked_user_id)
    )
    existing_like = existing_like.scalar_one_or_none()
    if not existing_like:
        like = UserLike(user_id=user_id, liked_user_id=liked_user_id)
        db_session.add(like)
        was_liked = UserWasLiked(user_id=liked_user_id, liked_user_id=user_id)
        db_session.add(was_liked)
        await db_session.commit()
        liked_user = await db_session.execute(select(User).where(User.user_id == liked_user_id))
        liked_user = liked_user.scalar_one_or_none()
        return liked_user

async def has_likes(db_session: AsyncSession, user_id: int) -> bool:
    result = await db_session.execute(select(UserWasLiked).filter(UserWasLiked.user_id == user_id))
    rows = result.scalars().all()
    return len(rows) > 0

async def get_was_liked_users(db_session: AsyncSession, user_id: int):
    result = await db_session.execute(
        select(User)
        .join(UserWasLiked, UserWasLiked.liked_user_id == User.user_id)
        .filter(UserWasLiked.user_id == user_id)
        .order_by(UserWasLiked.id)
    )
    liked_users = result.scalars().all()
    return liked_users

async def remove_from_was_liked(db_session: AsyncSession, user_id: int, liked_user_id: int):
    result = await db_session.execute(
        select(UserWasLiked).filter_by(user_id=user_id, liked_user_id=liked_user_id)
    )
    user_liked = result.scalar_one_or_none()
    if user_liked:
        await db_session.delete(user_liked)
        await db_session.commit()

async def make_match(db_session: AsyncSession, user_id: int, liked_user_id: int):
    user_like_exists = await db_session.execute(
        select(UserLike).filter_by(user_id=user_id, liked_user_id=liked_user_id)
    )
    user_like = user_like_exists.scalar_one_or_none()
    liked_user_like_exists = await db_session.execute(
        select(UserLike).filter_by(user_id=liked_user_id, liked_user_id=user_id)
    )
    liked_user_like = liked_user_like_exists.scalar_one_or_none()
    if user_like and liked_user_like:
        match = UserMatch(user_1_id=user_id, user_2_id=liked_user_id)
        db_session.add(match)
        await db_session.commit()
        return True 
    return False
