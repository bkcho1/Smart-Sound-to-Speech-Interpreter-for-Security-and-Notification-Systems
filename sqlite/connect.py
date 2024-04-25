from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlite.models import Base, Sound, Message, Fingerprint
from collections import defaultdict

from config import DATABASE_URI, DEV_MODE
from logic.fingerprint import fingerprint

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URI, echo=DEV_MODE)
Base.metadata.create_all(bind=engine)

# Create a sessionmaker to interact with the database
Session = sessionmaker(bind=engine)
    
def insert(name, data, message):
    # Create a session
    session = Session()

    try:
        # check if sound file already exists in database
        if session.query(Sound).filter_by(file_name=name).first() is None:
            new_sound = Sound(file_name=name,file=data)
            session.add(new_sound)
            session.commit()

            print(new_sound.id)
            new_message = Message(text=message, sound_id=new_sound.id)
            session.add(new_message)
            session.commit()

            for i in range(data.ndim):
                hashes = fingerprint(data[:,i])
                #print(tuple(hashes))
                for hash in hashes:
                    new_fingerprint = Fingerprint(hash=bytes.fromhex(hash[0]), sound_id=new_sound.id, offset=int(hash[1]))
                    session.add(new_fingerprint)
                    try:
                        session.commit()
                    except IntegrityError:
                        session.rollback()
            print("Insertion successfully")

            
        else:
            print('Error: file already is in database')
    except Exception as e:
        session.rollback()
        print(f"Error inserting data: {e}")
    finally:
        session.close()

def fetch():
    # Create a session
    session = Session()

    try:
        # Fetch all sound files and messages from the database
        info = []
        sounds = session.query(Sound).all()
        for sound in sounds:
            message = session.query(Message).filter_by(sound_id=sound.id).first()
            info.append({"File Name":f'{sound.file_name}', "ID":f'{sound.id}',"Message":f'{message.text}'})
        return info
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
    finally:
        session.close()

def update(id, new_message):
    # Create a session
    session = Session()

    try:
        session.query(Message).filter(Message.sound_id==id).update({'text': new_message})
        session.commit()
    except Exception as e:
        session.rollback()
        print(f'Error in updating data: {e}')
    finally:
        session.close()

def delete_sound(sound_id):
    # Create a session
    session = Session()

    try:
        # Find the sound file by ID and delete it from the database
        sound = session.query(Sound).filter(Sound.id == sound_id).first()
        if sound:
            session.delete(sound)
            session.commit()
            print("Sound file deleted successfully.")
        else:
            print("Sound file not found.")
    except Exception as e:
        session.rollback()
        print(f"Error deleting sound file: {e}")
    finally:
        session.close()

def get(sound_id):
    session = Session()

    try:
        sound = session.query(Sound).filter(Sound.id == sound_id).first()
    except Exception as e:
        print(f"Error fetching file: {e}")
    finally:
        session.close()

    return sound.file_name


def match(hashes):
    session = Session()

    matches = []
    countDict = defaultdict(int)

    for hash in hashes:
        matched_rows = session.query(Fingerprint).filter(Fingerprint.hash == bytes.fromhex(hash[0])).all()
        for match in matched_rows:
            countDict[match.sound_id]
            matches.append((match.sound_id, match.offset - hash[1]))

    for match in matches:
        countDict[match[0]] = countDict[match[0]] + 1

    session.close()

    return matches, countDict
