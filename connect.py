# from sqlalchemy import create_engine
# from models import Base, Sound, Message, Fingerprint
# from config import DATABASE_URI

# # establish connection with db
# engine = create_engine(DATABASE_URI, echo=True)

# # demo code, playing around with creating tables and stuff
# print('Creating tables...')
# Base.metadata.create_all(bind=engine)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Sound
from config import DATABASE_URI

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URI, echo=True)

# Create a sessionmaker to interact with the database
Session = sessionmaker(bind=engine)

def insert_sounds(file_paths):
    # Create a session
    session = Session()

    try:
        for file_path in file_paths:
            # Read the sound file and insert it into the database
            with open(file_path, 'rb') as file:
                sound_data = file.read()
            new_sound = Sound(file=sound_data)
            session.add(new_sound)

        session.commit()
        print("Sound files inserted successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error inserting sound files: {e}")
    finally:
        session.close()

def fetch_sounds():
    # Create a session
    session = Session()

    try:
        # Fetch all sound files from the database
        sounds = session.query(Sound).all()
        return sounds
    except Exception as e:
        print(f"Error fetching sound files: {e}")
        return []
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
    # Example usage: Insert sound files
    file_paths = ['sounds/sound1.wav', 'sounds/sound2.wav', 'sounds/sound3.wav']
    # insert_sounds(file_paths)

    # Example usage: Fetch all sound files
    # sounds = fetch_sounds()
    # for sound in sounds:
    #     print(f"Sound ID: {sound.id}")

    # Example usage: Delete a sound file (replace sound_id with the actual ID)
    sound_id = 1
    # delete_sound(5)
    # delete_sound(6)
    # delete_sound(7)
    def menu():
        while True:
            print("Options:")
            print("1. Insert sound")
            print("2. Fetch sound")
            print("3. Delete sound")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                file_paths = input("Enter file paths (separated by comma): ").split(",")
                insert_sounds(file_paths)
            elif choice == "2":
                sounds = fetch_sounds()
                for sound in sounds:
                    print(f"Sound ID: {sound.id}")
            elif choice == "3":
                sound_id = input("Enter sound ID to delete: ")
                delete_sound(sound_id)
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")

    menu()