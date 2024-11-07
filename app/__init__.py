import os
import re

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from openai import OpenAI

from .config import Config
from .droneflights import droneflights

# Initialize Flask app
app = Flask(__name__, static_folder='../react-drone/build',
            static_url_path='/')
CORS(app)

app.config.from_object(Config)


def ordinal_to_number(ordinal_word):
    ordinal_map = {
        "first": 1, "second": 2, "third": 3, "fourth": 4,
        "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
        "ninth": 9, "tenth": 10
    }
    return ordinal_map.get(ordinal_word, None)


# Mapping of subject keywords to fields in the droneflight records
subject_field_map = {
    "image id": "image_id",
    "timestamp": "timestamp",
    "altitude": "altitude_m",
    "battery": "battery_level_pct",
    "speed": "drone_speed_mps",
    "heading": "heading_deg",
    "latitude": "latitude",
    "longitude": "longitude",
    "image": "image_id",
    "camera tilt": "camera_tilt_deg",
    "focal length": "focal_length_mm",
    "iso": "iso",
    "shutter speed": "shutter_speed",
    "aperture": "aperture",
    "color temperature": "color_temp_k",
    "file size": "file_size_mb",
    "gps accuracy": "gps_accuracy_m",
    "gimbal mode": "gimbal_mode",
    "subject detection": "subject_detection",
    "heading degree": "heading_deg",
    "file name": "file_name",
    "image format": "image_format",
    "drone speed": "drone_image"
}


@app.route("/api/droneflights")
def index():
    return jsonify(droneflights)



@app.route("/api/test", methods=["POST"])
def query():
    try:
        data = request.get_json()
        query = data.get("query", "").lower()
        # Set the OpenAI API key from the environment variable
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Call OpenAI API with the query
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Extract the subject and number from the following sentence: {query}. Only return the subject and number in a clear format, like 'Subject: [subject], Number: [number]'."
                }
            ],
            max_tokens=100,
        )

        generated_text = response.choices[0].message.content.strip()

        subject_match = re.search(r'Subject: (\w+)', generated_text)
        number_match = re.search(r'Number: (\d+)', generated_text)

        print(response, subject_match, number_match)
        # Handle missing matches or data
        if not subject_match or not number_match:
            return jsonify({"response": "Could not parse subject or number from the response."}), 200

        # Parse extracted information
        subject = subject_match.group(1).lower()
        number_text = number_match.group(1)

        # Map the subject to a field in the data
        field = subject_field_map.get(subject)
        if not field:
            return jsonify({"response": f"Unknown subject: {subject}."}), 200

        # Convert number text to an index, making sure it’s within bounds
        index = int(number_text) - 1
        if index < 0 or index >= len(droneflights):
            return jsonify({"response": f"No record found for the {number_text} entry."}), 200

        # Retrieve and return the data
        record = droneflights[index]
         # Retrieve the requested data
        response_data = f"The {subject} for the {index} entry is {record.get(field, 'not available')}."
        return jsonify({"response": response_data}), 200

    except Exception as e:
        # Print the error to the Flask console for debugging
        print("Error processing query:", e)
        return jsonify({"error": "An internal error occurred"}), 500


# Serve the React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
