import threading
import csv
from datetime import datetime, timedelta
import webbrowser
from flask import Flask, render_template, request, jsonify
from sqlite.connect import insert, fetch_message, fetch_all, update, delete_sound, insert_log, get_session
from config import SOUNDS, TEST  # Import TEST for the "test" folder path
from logic.file_utils import read
from logic.sound_recognition import record_then_recognize, recognize
from datetime import datetime
from logic.sound_IO import record_audio, play_text   # Import the record_audio function
from sqlite.models import Log
import os



app = Flask(__name__)



# Define routes for the web GUI

@app.route('/')
def home():
    return render_template('admin.html')

@app.route('/logs', methods=['GET'])
def logs_page():
    session = get_session()
    try:
        # Fetch all logs from the database
        logs = session.query(Log).all()
        return render_template('logs.html', logs=logs)
    except Exception as e:
        print(f"Error loading logs: {e}")
        return "Error loading logs", 500
    finally:
        session.close()


@app.route('/insert', methods=['POST'])
def insert_entry():
    file_name = request.form['file_name']
    message = request.form['message']
    
    file_path = os.path.join(SOUNDS, file_name)
    if not os.path.isfile(file_path):
        return jsonify({'status': 'Error', 'message': 'File not found in the sounds folder'}), 400
    
    data = read(file_name, SOUNDS)
    if data is None:
        return jsonify({'status': 'Error', 'message': 'Unable to read file data'}), 400
    
    insert(file_name, data, message)
    return jsonify({'status': 'Entry inserted successfully'})


@app.route('/fetch', methods=['GET'])
def fetch_entries():
    entries = fetch_all()
    return jsonify(entries)

@app.route('/fetch_test_files', methods=['GET'])
def fetch_test_files():
    try:
        files = os.listdir(TEST)
        return jsonify(files)
    except Exception as e:
        print(f"Error fetching test files: {e}")
        return jsonify([])



@app.route('/update', methods=['POST'])
def update_entry():
    sound_id = request.form['sound_id']
    new_message = request.form['new_message']
    update(sound_id, new_message)
    return jsonify({'status': 'Entry updated successfully'})

@app.route('/delete', methods=['POST'])
def delete_entry():
    sound_id = request.form['sound_id']
    delete_sound(sound_id)
    return jsonify({'status': 'Entry deleted successfully'})

# @app.route('/recognize', methods=['POST'])
# def recognize_route():
#     try:
#         file_name = request.form['file_name']
#         if not file_name:
#             return jsonify({'status': 'Error', 'message': 'No file selected for recognition.'})

#         file_path = os.path.join(TEST, file_name)
#         if not os.path.isfile(file_path):
#             message = 'File not found in the test folder.'
#             print(message)
#             return jsonify({'status': 'Recognition failed', 'message': message})

#         # Perform recognition against sounds in the "sounds" folder
#         status, sound_id, output = recognize(file_name, TEST)
#         if status == -1:
#             message = 'Analyzed sound does not match with stored sounds.'
#             return jsonify({'status': 'Recognition failed', 'message': message})
#         else:
#             message = fetch_message(sound_id)
#             return jsonify({'status': 'Recognition successful', 'predicted_file': output, 'message': message})
#     except Exception as e:
#         message = f'An error occurred: {str(e)}'
#         return jsonify({'status': 'Error', 'message': message})

    

# # File: app.py new code for logs

@app.route('/recognize', methods=['POST'])
def recognize_sound():
    try:
        file_name = request.form['file_name']
        file_path = os.path.join(TEST, file_name)

        if not os.path.isfile(file_path):
            message = 'File not found in the test folder.'
            print(message)
            insert_log(file_name, message)  # Log the event
            return jsonify({'status': 'Recognition failed', 'message': message})

        status, sound_id, output = recognize(file_name, TEST)
        if status == -1:
            message = 'Analyzed sound does not match with stored sounds.'
            print(message)
            insert_log(file_name, message)  # Log the event
            return jsonify({'status': 'Recognition failed', 'message': message})
        else:
            message = fetch_message(sound_id)
            print(f"Match found: {message}")
            insert_log(file_name, message)  # Log the event
            return jsonify({'status': 'Recognition successful', 'predicted_file': output, 'message': message})
    except Exception as e:
        message = f'An error occurred: {str(e)}'
        print(message)
        insert_log('Unknown', message)  # Log the error
        return jsonify({'status': 'Error', 'message': message})



# This code records audio and recognizes it
@app.route('/record_audio', methods=['POST'])
def record_audio_route():
    try:
        # Use the `record_then_recognize` function to record and recognize
        status, sound_id, output = record_then_recognize(TEST)
        if status == -1:
            message = "Analyzed sound is not similar enough to stored sounds."
        else:
            message = fetch_message(sound_id)

        # Log the recognition attempt
        insert_log(output if status != -1 else 'Unknown', message)

        # Return the response to be used by the frontend
        return jsonify({'status': 'Recognition successful' if status != -1 else 'Recognition failed', 'message': message})
    except Exception as e:
        message = f'An error occurred: {str(e)}'
        print(message)
        return jsonify({'status': 'Error', 'message': message}), 500


    

# This code fetches the data to logs page
@app.route('/fetch_logs', methods=['GET'])
def fetch_logs():
    session = get_session()
    try:
        logs = session.query(Log).all()
        log_data = [
            {
                'id': log.id,
                'File Name': log.file_name,
                'Message': log.message,
                'Timestamp': log.timestamp.strftime('%A, %d %B %Y %H:%M:%S')
            }
            for log in logs
        ]
        print(f"Logs Fetched: {log_data}")  # Debugging line
        return jsonify(log_data)
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return jsonify([])
    finally:
        session.close()

# @app.route('/delete_logs', methods=['POST'])
# def delete_logs():
#     try:

#         print(f"Incoming delete request data: {request.data}")  # Debugging line

#         data = request.get_json()
#         log_ids = data.get('log_ids', [])

#         print(f"Log IDs received for deletion: {log_ids}")  # Debugging line

#         # Validate received log_ids and filter out any non-integer or 'undefined' values
#         valid_log_ids = []
#         for log_id in log_ids:
#             try:
#                 valid_log_ids.append(int(log_id))
#             except ValueError:
#                 print(f"Invalid log ID received: {log_id}")  # Log the invalid ID

#         if not valid_log_ids:
#             return jsonify({'status': 'Error', 'message': 'No valid log IDs provided'}), 400

#         # Proceed with backup and deletion of valid log entries
#         session = get_session()
#         logs_to_delete = session.query(Log).filter(Log.id.in_(valid_log_ids)).all()

#         # Backup to CSV
#         backup_file_path = 'backup_logs.csv'
#         file_exists = os.path.isfile(backup_file_path)

#         with open(backup_file_path, mode='a', newline='') as csv_file:
#             fieldnames = ['id', 'file_name', 'message', 'timestamp']
#             writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#             if not file_exists:
#                 writer.writeheader()

#             for log in logs_to_delete:
#                 writer.writerow({
#                     'id': log.id,
#                     'file_name': log.file_name,
#                     'message': log.message,
#                     'timestamp': log.timestamp.strftime('%A, %d %B %Y %H:%M:%S')
#                 })

#         # Delete logs from the database
#         session.query(Log).filter(Log.id.in_(valid_log_ids)).delete(synchronize_session=False)
#         session.commit()

#         session.close()
#         return jsonify({'status': 'Success', 'message': 'Selected logs backed up and deleted successfully'})

#     except Exception as e:
#         print(f"Error processing delete request: {e}")
#         return jsonify({'status': 'Error', 'message': 'An error occurred while processing logs deletion'}), 500

    
    
# Function to schedule the backup and cleanup every 24 hours    
# Backup and Cleanup Logic
def backup_and_cleanup_old_logs():
    session = get_session()
    try:
        # Calculate the date 15 days ago from today
        cutoff_date = datetime.now() - timedelta(days=15)

        # Query logs older than 15 days
        old_logs = session.query(Log).filter(Log.timestamp < cutoff_date).all()

        if old_logs:
            # Write old logs to a backup CSV file
            backup_file = 'logs_backup.csv'
            with open(backup_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                # Write header if the file is empty
                if file.tell() == 0:
                    writer.writerow(['File Name', 'Message', 'Timestamp'])
                # Write each old log to the CSV
                for log in old_logs:
                    writer.writerow([log.file_name, log.message, log.timestamp.strftime('%Y-%m-%d %H:%M:%S')])
            
            # Delete the old logs from the database
            for log in old_logs:
                session.delete(log)
            session.commit()
            print(f"Backed up and deleted {len(old_logs)} logs successfully.")
        else:
            print("No logs older than 15 days found for backup and deletion.")
    except Exception as e:
        print(f"Error during backup and cleanup: {e}")
        session.rollback()
    finally:
        session.close()

# Function to schedule the backup and cleanup every 24 hours
def schedule_backup_and_cleanup():
    backup_and_cleanup_old_logs()
    # Schedule the next execution after 24 hours (86400 seconds)
    threading.Timer(86400, schedule_backup_and_cleanup).start()


def open_browser():
    """Function to open the default web browser after a slight delay."""
    webbrowser.open('http://127.0.0.1:5000/') # Open the web browser at the URL of the Flask app

if __name__ == "__main__":
    # Start the Flask server and open the web GUI
    print("Starting Flask server and scheduling backup...")
    threading.Timer(1, open_browser).start()
    # Schedule the first backup
    schedule_backup_and_cleanup()
    # Run the Flask application
    app.run(debug=True, use_reloader=False, port=5000)



# import threading
# import webbrowser
# from flask import Flask, render_template, request, jsonify
# from sqlite.connect import insert, fetch_message, fetch_all, update, delete_sound, get_session
# from config import SOUNDS, TEST  # Import TEST for the "test" folder path
# from logic.file_utils import read
# from logic.sound_recognition import record_then_recognize, recognize
# from datetime import datetime
# from logic.sound_IO import record_audio, play_text   # Import the record_audio function
# from sqlite.models import Log
# # from sqlalchemy.orm import sessionmaker
# # from sqlite.connect import engine
# import os

# app = Flask(__name__)

# # Session = sessionmaker(bind=engine)

# # Define routes for the web GUI

# @app.route('/')
# def home():
#     return render_template('admin.html')

# @app.route('/logs', methods=['GET'])
# def logs_page():
#     session = get_session()
#     try:
#         # Fetch all logs from the database
#         logs = session.query(Log).all()
#         return render_template('logs.html', logs=logs)
#     except Exception as e:
#         print(f"Error loading logs: {e}")
#         return "Error loading logs", 500
#     finally:
#         session.close()

# @app.route('/insert', methods=['POST'])
# def insert_entry():
#     file_name = request.form['file_name']
#     message = request.form['message']
    
#     file_path = os.path.join(SOUNDS, file_name)
#     if not os.path.isfile(file_path):
#         return jsonify({'status': 'Error', 'message': 'File not found in the sounds folder'}), 400
    
#     data = read(file_name, SOUNDS)
#     if data is None:
#         return jsonify({'status': 'Error', 'message': 'Unable to read file data'}), 400
    
#     insert(file_name, data, message)
#     return jsonify({'status': 'Entry inserted successfully'})


# @app.route('/fetch', methods=['GET'])
# def fetch_entries():
#     entries = fetch_all()
#     return jsonify(entries)

# @app.route('/fetch_test_files', methods=['GET'])
# def fetch_test_files():
#     try:
#         files = os.listdir(TEST)
#         return jsonify(files)
#     except Exception as e:
#         print(f"Error fetching test files: {e}")
#         return jsonify([])



# @app.route('/update', methods=['POST'])
# def update_entry():
#     sound_id = request.form['sound_id']
#     new_message = request.form['new_message']
#     update(sound_id, new_message)
#     return jsonify({'status': 'Entry updated successfully'})

# @app.route('/delete', methods=['POST'])
# def delete_entry():
#     sound_id = request.form['sound_id']
#     delete_sound(sound_id)
#     return jsonify({'status': 'Entry deleted successfully'})

# @app.route('/recognize', methods=['POST'])
# def recognize_route():
#     try:
#         file_name = request.form['file_name']
#         if not file_name:
#             return jsonify({'status': 'Error', 'message': 'No file selected for recognition.'})

#         file_path = os.path.join(TEST, file_name)
#         if not os.path.isfile(file_path):
#             message = 'File not found in the test folder.'
#             print(message)
#             return jsonify({'status': 'Recognition failed', 'message': message})

#         # Perform recognition against sounds in the "sounds" folder
#         status, sound_id, output = recognize(file_name, TEST)
#         if status == -1:
#             message = 'Analyzed sound does not match with stored sounds.'
#             return jsonify({'status': 'Recognition failed', 'message': message})
#         else:
#             message = fetch_message(sound_id)
#             return jsonify({'status': 'Recognition successful', 'predicted_file': output, 'message': message})
#     except Exception as e:
#         message = f'An error occurred: {str(e)}'
#         return jsonify({'status': 'Error', 'message': message})

    

# # # File: app.py new code for logs

# # @app.route('/recognize', methods=['POST'])
# # def recognize_sound():
# #     try:
# #         file_name = request.form['file_name']
# #         file_path = os.path.join(TEST, file_name)

# #         if not os.path.isfile(file_path):
# #             message = 'File not found in the test folder.'
# #             print(message)
# #             insert_log(file_name, message)  # Log the event
# #             return jsonify({'status': 'Recognition failed', 'message': message})

# #         status, sound_id, output = recognize(file_name, TEST)
# #         if status == -1:
# #             message = 'Analyzed sound does not match with stored sounds.'
# #             print(message)
# #             insert_log(file_name, message)  # Log the event
# #             return jsonify({'status': 'Recognition failed', 'message': message})
# #         else:
# #             message = fetch_message(sound_id)
# #             print(f"Match found: {message}")
# #             insert_log(file_name, message)  # Log the event
# #             return jsonify({'status': 'Recognition successful', 'predicted_file': output, 'message': message})
# #     except Exception as e:
# #         message = f'An error occurred: {str(e)}'
# #         print(message)
# #         insert_log('Unknown', message)  # Log the error
# #         return jsonify({'status': 'Error', 'message': message})



# @app.route('/record_audio', methods=['POST'])
# def record_audio_route():
#     try:
#         # Use the `record_then_recognize` function to record and recognize
#         status, sound_id, output = record_then_recognize(TEST)
#         if status == -1:
#             message = "Analyzed sound is not similar enough to stored sounds."
#         else:
#             message = fetch_message(sound_id)
        
#         # # Log the recognition attempt
#         # insert_log(output if status != -1 else 'Unknown', message)

#         # # Print the message to logs
#         # print(message)

#         # Return the response to be used by the frontend
#         return jsonify({'status': 'Recognition successful' if status != -1 else 'Recognition failed', 'message': message})
#     except Exception as e:
#         message = f'An error occurred: {str(e)}'
#         print(message)
#         return jsonify({'status': 'Error', 'message': message}), 500


    

# # This code fetches the data to logs page
# @app.route('/fetch_logs', methods=['GET'])
# def fetch_logs():
#     session = Session()
#     try:
#         logs = session.query(Log).all()
#         log_data = []
#         for log in logs:
#             log_data.append({
#                 'File Name': log.file_name,
#                 'Message': log.message,
#                 'Timestamp': log.timestamp.strftime('%A, %d %B %Y %H:%M:%S')
#             })
#         return jsonify(log_data)
#     except Exception as e:
#         print(f"Error fetching logs: {e}")
#         return jsonify([])
#     finally:
#         session.close()

    


# def open_browser():
#     """Function to open the default web browser after a slight delay."""
#     webbrowser.open_new('http://127.0.0.1:5000/') # Open the web browser at the URL of the Flask app

# if __name__ == "__main__":
#     # Open the browser in a separate thread after a slight delay
#     print("Starting Flask server and opening the web GUI...")
#     threading.Timer(1, open_browser).start()
#     # Run the Flask application
#     app.run(debug=True, use_reloader=False)