import threading
import webbrowser
from flask import Flask, render_template, request, jsonify
from sqlite.connect import insert, fetch_message, fetch_all, update, delete_sound
from config import SOUNDS
from logic.file_utils import read
from logic.sound_recognition import recognize
from datetime import datetime
from logic.sound_IO import record_audio  # Import the record_audio function
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
    file_name = request.form['file_name']
    status, sound_id, output = recognize(file_name, SOUNDS)
    if status == -1:
        return jsonify({'status': 'Recognition failed', 'message': output})
    else:
        message = fetch_message(sound_id)
        return jsonify({'status': 'Recognition successful', 'predicted_file': output, 'message': message})

@app.route('/record_audio', methods=['POST'])
def record_audio_route():
    # Create a filename with a timestamp to avoid overwriting files
    filename = f"mic_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    record_audio(filename)
    return jsonify({'status': 'Recording complete', 'filename': filename})

def open_browser():
    """Function to open the default web browser after a slight delay."""
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
    # Open the browser in a separate thread after a slight delay
    print("Starting Flask server and opening the web GUI...")
    threading.Timer(1, open_browser).start()
    # Run the Flask application
    app.run(debug=True, use_reloader=False)
