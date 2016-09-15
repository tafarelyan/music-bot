from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from credentials import ENGINE


Base = declarative_base()


class Backup(Base):
    __tablename__ = 'backup'

    id = Column(Integer, primary_key=True)
    title = Column(String(120))
    video_url = Column(String(120))


Base.metadata.create_all(ENGINE)
