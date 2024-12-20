from sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, DateTime
# from .connect import get_session

# boilerplate, needed for other classes
class Base(DeclarativeBase):
    pass

# sound file table
class Sound(Base):
    __tablename__ = 'sounds'
    id = Column(Integer, primary_key=True)
    file_name = Column(String, unique=True, nullable=False)
    file = Column(LargeBinary, nullable=False)

    messages = relationship('Message',cascade='all, delete-orphan')
    fingerprints = relationship('Fingerprint',cascade='all, delete-orphan')

# text message table
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer,primary_key=True)
    text = Column(String,nullable=False)
    sound_id = Column(Integer,ForeignKey('sounds.id'),unique=True,nullable=False)

# acoustic fingerprint table
class Fingerprint(Base):
    __tablename__ = 'fingerprints'
    __table_args__ = (
        PrimaryKeyConstraint('hash', 'sound_id', 'offset'),
    )
    hash = Column(BINARY(10),nullable=False,unique=True,index=True)
    sound_id = Column(Integer,ForeignKey('sounds.id'),nullable=False)
    offset = Column(Integer)

    # # code to insert recorded sound into the database
    # def insert_sound(file_path):
    #     with open(file_path, 'rb') as file:
    #         sound_data = file.read()
    #     sound = Sound(file=sound_data)
    #     get_session.add(sound)
    #     get_session.commit()

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)