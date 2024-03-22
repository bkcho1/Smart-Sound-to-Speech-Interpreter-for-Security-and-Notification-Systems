from sqlalchemy import create_engine
from models import Base, Sound, Message, Fingerprint
from config import DATABASE_URI

# establish connection with db
engine = create_engine(DATABASE_URI, echo=True)

# demo code, playing around with creating tables and stuff
print('Creating tables...')
Base.metadata.create_all(bind=engine)