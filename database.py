from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select
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
    user = await get_user_data(user_data.get('user_id'))
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
