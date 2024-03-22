from sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# boilerplate, needed for other classes
class Base(DeclarativeBase):
    pass

# sound file table
class Sound(Base):
    __tablename__ = 'sounds'
    id = Column(Integer, primary_key=True)
    file = Column(LargeBinary, nullable=False)

# text message table
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer,primary_key=True)
    text = Column(String,nullable=False)
    sound_id = Column(Integer,ForeignKey('sound.id'),unique=True,nullable=False)

# acoustic fingerprint table
class Fingerprint(Base):
    __tablename__ = 'fingerprints'
    hash = Column(BINARY(10),primary_key=True,nullable=False,index=True,unique=True)
    sound_id = Column(Integer,ForeignKey('sound.id'),unique=True,nullable=False)
    offset = Column(Integer,unique=True)

