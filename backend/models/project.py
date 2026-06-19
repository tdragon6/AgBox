'''
项目管理 数据库模型
'''


from datetime import datetime, timezone

from core.database import Base
from sqlalchemy import JSON, Column, DateTime, String


class Project(Base):
    __tablename__ = 'project'

    id = Column(String, primary_key=True, index=True, nullable=False, comment='主键ID')
    name = Column(String, nullable=False, comment='项目名称')
    description = Column(String, nullable=False, comment='项目描述')
    robots = Column(JSON, nullable=False, comment='数字员工')
    history_robots = Column(JSON, nullable=False, comment='历史数字员工')
    created_time = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), comment='创建时间')
    updated_time = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), comment='更新时间')
