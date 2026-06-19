'''
数据库配置
'''


from typing import Generator

from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

db_engine = create_engine(
    settings.DATABASE_URL,
    connect_args={'check_same_thread': False}
)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = db_session()
    try:
        yield db
    finally:
        db.close()