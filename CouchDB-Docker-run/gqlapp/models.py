from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

#from db_conf import Base
from sqlalchemy.ext.declarative import declarative_base


class Post(declarative_base()):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    content = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())