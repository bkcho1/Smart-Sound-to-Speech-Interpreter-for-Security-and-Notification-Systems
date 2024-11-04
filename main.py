from sqlite.connect import insert, fetch_message, fetch_all, update, delete_sound
from config import SOUNDS, TEST
from logic.file_utils import read
from logic.sound_recognition import recognize, record_then_recognize
from logic.sound_IO import play_text
import os

# Demo usage
if __name__ == "__main__":
    def menu():
        while True:
            print("Options:")
            print("1. Insert an entry")
            print("2. Fetch data")
            print("3. Update an entry")
            print("4. Delete an entry")
            print("5. Recognize a sound")
            print("6. Record than recognize a sound")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                print("Available sound files:", end=" ")
                print(os.listdir(SOUNDS))
                file_name = input("Please choose a file: ")
                message = input("Enter a message: ")
                data = read(file_name, SOUNDS)
                insert(file_name, data, message)
            elif choice == "2":
                list = fetch_all()
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
            elif choice == "5":
                print("Available sound files:", end=" ")
                print(os.listdir(TEST))
                file_name = input("Please choose a file: ")
                status, sound_id, output = recognize(file_name, TEST)
                if status == -1:
                    print(output)
                else:
                    message = fetch_message(sound_id)
                    print("Predicted file is " + output + " and has message: \"" + message + "\"")
                    #play_text(message)
            elif choice == "6":
                status, sound_id, output = record_then_recognize(SOUNDS)
                if status == -1:
                    print(output)
                else:
                    message = fetch_message(sound_id)
                    print("Predicted file is " + output + " and has message: \"" + message + "\"")
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
            print()
    menu()