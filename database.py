import boto3
from sqlalchemy import Column, Integer, String, BigInteger, ARRAY
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select
from sqlalchemy.sql.expression import func
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
    viewed_users = Column(ARRAY(BigInteger), default=[])
    liked_users = Column(ARRAY(BigInteger), default=[])

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
    if not user.viewed_users:
        user.viewed_users = []
    result = await db_session.execute(
        select(User).where(
            User.user_id != user_id,
            ~User.user_id.in_(user.viewed_users)
        ).order_by(func.random())
    )
    next_user = result.scalars().first()
    return next_user

async def add_viewed_user(db_session: AsyncSession, user_id: int, viewed_user_id: int):
    result = await db_session.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return
    if not user.viewed_users:
        user.viewed_users = []
    if viewed_user_id not in user.viewed_users:
        user.viewed_users.append(viewed_user_id)
        await db_session.commit()

async def liked_user(db_session: AsyncSession, user_id: int, liked_user_id: int):
    result = await db_session.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    if not user.liked_users:
        user.liked_users = []
    user.liked_users.append(liked_user_id)
    await db_session.commit()
