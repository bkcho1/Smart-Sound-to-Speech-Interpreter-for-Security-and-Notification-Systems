from flask import Flask, jsonify, request, render_template
from datetime import datetime
import os
from logic.mic_input import record_audio
from logic.sound_recognition import recognize
from sqlite.connect import fetch, insert, update, delete_sound
from config import SOUNDS

app = Flask(__name__)

# Serve the HTML page for the admin interface
@app.route('/')
def admin_panel():
    return render_template('admin.html')

# API to insert a new sound entry
@app.route('/insert', methods=['POST'])
def insert_entry():
    file_name = request.form['file_name']
    message = request.form['message']
    
    # Check if the file exists in the SOUNDS directory
    file_path = os.path.join(SOUNDS, file_name)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    with open(file_path, 'rb') as f:
        sound_data = f.read()

    # Insert the sound file and message into the database
    insert(file_name, sound_data, message)
    return jsonify({"message": "Entry inserted successfully!"})

# API to fetch all sound entries
@app.route('/fetch', methods=['GET'])
def fetch_entries():
    data = fetch()  # Fetch data from the database
    return jsonify(data)

# API to update a sound entry's message
@app.route('/update', methods=['POST'])
def update_entry():
    sound_id = request.form['sound_id']
    new_message = request.form['new_message']
    update(sound_id, new_message)
    return jsonify({"message": "Entry updated successfully!"})

# API to delete a sound entry
@app.route('/delete', methods=['POST'])
def delete_entry():
    sound_id = request.form['sound_id']
    delete_sound(sound_id)
    return jsonify({"message": "Entry deleted successfully!"})

# API to recognize a sound from a file
@app.route('/recognize', methods=['POST'])
def recognize_sound():
    file_name = request.form['file_name']
    result = recognize(file_name, SOUNDS)
    return jsonify({"message": f"Recognized sound: {result}"})

if __name__ == '__main__':
    app.run(debug=True)
