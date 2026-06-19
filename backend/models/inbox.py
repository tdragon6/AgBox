'''
收件箱 数据库模型
'''


from datetime import datetime, timezone

from core.database import Base
from sqlalchemy import Column, DateTime, String, Boolean


class Inbox(Base):
    __tablename__ = 'inbox'

    id = Column(String, primary_key=True, index=True, nullable=False, comment='主键ID')
    robot = Column(String, nullable=False, comment='数字员工名称')
    type = Column(String, nullable=False, comment='通知类型')
    message = Column(String, nullable=False, comment='任务消息')
    status = Column(String, nullable=False, comment='任务/升级状态')
    result = Column(String, nullable=False, comment='通知结果')
    is_read = Column(Boolean, nullable=False, default=False, comment='是否已读')
    coordinator = Column(Boolean, nullable=False, comment='是否为协调器')
    created_time = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), comment='创建时间')
    updated_time = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), comment='更新时间')
