'''
模型管理 数据库模型
'''


from datetime import datetime, timezone

from core.database import Base
from sqlalchemy import Column, DateTime, String


class Model(Base):
    __tablename__ = 'model'

    id = Column(String, primary_key=True, index=True, nullable=False, comment='主键ID')
    name = Column(String, nullable=False, comment='模型配置名称')
    provider_id = Column(String, nullable=False, comment='模型提供商ID')
    provider_name = Column(String, nullable=False, comment='模型提供商名称')
    model = Column(String, nullable=False, comment='模型名称')
    base_url = Column(String, nullable=False, comment='模型Base Url')
    api_key = Column(String, nullable=False, default='', comment='模型API密钥')
    created_time = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), comment='创建时间')
    updated_time = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), comment='更新时间')
