from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Sound, Message
from config import DATABASE_URI, SOUNDS
import os

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URI, echo=False)
Base.metadata.create_all(bind=engine)

# Create a sessionmaker to interact with the database
Session = sessionmaker(bind=engine)

def insert(name, data, message):
    # Create a session
    session = Session()

    try:
        # check if sound file already ecists in database
        if session.query(Sound).filter_by(file_name=name).first() is None:
            new_sound = Sound(file_name=name,file=data)
            session.add(new_sound)
            session.commit()
            print("Sound file inserted successfully.")

            new_message = Message(text=message, sound_id=new_sound.id)
            session.add(new_message)
            session.commit()
            print("Message inserted successfully.")
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

# Demo usage
if __name__ == "__main__":
    def menu():
        while True:
            print("Options:")
            print("1. Insert an entry")
            print("2. Fetch data")
            print("3. Update an entry")
            print("4. Delete an entry")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                print("Available sound files:", end=" ")
                print(os.listdir(SOUNDS))
                file_name = input("Please choose a file: ")
                with open(SOUNDS + '/' + file_name, 'rb') as file:
                    message = input("Enter a message: ")
                    data = file.read()
                    insert(file_name, data, message)
            elif choice == "2":
                list = fetch()
                if list:
                    for info in list:
                        print("Entry has name " + info["File Name"] + " with an ID of " + info["ID"] + " and has message " + '"' + info["Message"] + '".')
                else:
                    print("No info to print")
            elif choice == "3":
                sound_id = input("Enter sound ID to update: ")
                new_message = input("Enter a new message: ")
                update(sound_id, new_message)
            elif choice == "4":
                sound_id = input("Enter sound ID to delete: ")
                delete_sound(sound_id)
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
            print()

    menu()