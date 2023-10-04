from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.utils.config import settings
from sqlalchemy.exc import OperationalError
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


engine = create_async_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)

Base = declarative_base()


async def get_db():
    try:
        async with SessionLocal() as db:
            yield db
    except OperationalError as e:
        if 'DB server has gone away' in str(e):
            logger.info(str(e))
    finally:
        db.close()
