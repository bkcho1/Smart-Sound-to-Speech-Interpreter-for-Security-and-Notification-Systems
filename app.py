import threading
import webbrowser
from flask import Flask, render_template, request, jsonify
from sqlite.connect import insert, fetch_message, fetch_all, update, delete_sound
from config import SOUNDS, TEST  # Import TEST for the "test" folder path
from logic.file_utils import read
from logic.sound_recognition import recognize
from datetime import datetime
from logic.sound_IO import record_audio, play_text   # Import the record_audio function
import os

app = Flask(__name__)

# Define routes for the web GUI

@app.route('/')
def home():
    return render_template('admin.html')

@app.route('/insert', methods=['POST'])
def insert_entry():
    file_name = request.form['file_name']
    message = request.form['message']
    data = read(file_name, SOUNDS)
    insert(file_name, data, message)
    return jsonify({'status': 'Entry inserted successfully'})

@app.route('/fetch', methods=['GET'])
def fetch_entries():
    entries = fetch_all()
    return jsonify(entries)

@app.route('/fetch_test_files', methods=['GET'])
def fetch_test_files():
    files = os.listdir(TEST)
    return jsonify(files)


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

@app.route('/recognize', methods=['POST'])
def recognize_sound():
    try:
        file_name = request.form['file_name']
        file_path = os.path.join(TEST, file_name)

        # Check if the file exists in the "test" folder
        if not os.path.isfile(file_path):
            message = 'File not found in the test folder.'
            print(message)
            return jsonify({'status': 'Recognition failed', 'message': message})

        # Perform recognition against sounds in the "sounds" folder
        status, sound_id, output = recognize(file_name, TEST)
        if status == -1:
            message = 'Analyzed sound does not match with stored sounds.'
            print(message)
            return jsonify({'status': 'Recognition failed', 'message': message})
        else:
            message = fetch_message(sound_id)
            print(f"Match found: {message}")
            return jsonify({'status': 'Recognition successful', 'predicted_file': output, 'message': message})

    except Exception as e:
        # Catch unexpected errors and log them for debugging
        message = f'An error occurred: {str(e)}'
        print(message)
        return jsonify({'status': 'Error', 'message': message})


@app.route('/record_audio', methods=['POST'])
def record_audio_route():
    # Create a filename with a timestamp to avoid overwriting files
    filename = f"mic_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    file_path = os.path.join(TEST, filename)  # Use TEST to save in the "test" folder
    record_audio(file_path)  # Pass the full path to record_audio
    status, sound_id, output = recognize(filename, TEST)
    if status == -1:
        message = "Analyzed sound is not similar enough to stored sounds."
        print(message)
        play_text(message)
        return jsonify({'status': 'Recognition failed', 'message': message})
    else:
        message = fetch_message(sound_id)
        print(f"Match found: {message}")
        play_text(message)
        return jsonify({'status': 'Recognition successful', 'predicted_file': output, 'message': message})
    


def open_browser():
    """Function to open the default web browser after a slight delay."""
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
    # Open the browser in a separate thread after a slight delay
    print("Starting Flask server and opening the web GUI...")
    threading.Timer(1, open_browser).start()
    # Run the Flask application
    app.run(debug=True, use_reloader=False)
