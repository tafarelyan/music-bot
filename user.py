from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text


engine = create_engine('sqlite:///musicbot.db')
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    title = Column(String)
    video_url = Column(Text)

Base.metadata.create_all(engine)
