'''
任务管理 数据库模型
'''


from datetime import datetime, timezone

from core.database import Base
from sqlalchemy import JSON, Column, DateTime, Integer, String


class Task(Base):
    __tablename__ = 'task'

    id = Column(String, primary_key=True, index=True, nullable=False, comment='主键ID')
    message = Column(String, nullable=False, comment='任务消息')
    project_id = Column(String, nullable=False, comment='项目ID')
    type = Column(String, nullable=False, comment='任务类型')
    priority = Column(String, nullable=False, default='P3', comment='任务优先级')
    status = Column(String, nullable=False, default='pending', comment='任务状态')
    robots = Column(JSON, nullable=False, comment='数字员工')
    trigger = Column(String, nullable=False, comment='触发来源')
    result = Column(String, nullable=False, default='', comment='任务结果')
    thread_id = Column(Integer, nullable=False, default=0, comment='线程ID')
    created_time = Column(DateTime, nullable=True, comment='创建时间')
    updated_time = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), comment='更新时间')
